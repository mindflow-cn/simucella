(() => {
  const menu = document.querySelector('.paper-menu');
  const links = document.querySelector('.paper-nav-links');
  if (menu && links) {
    menu.addEventListener('click', () => {
      const open = links.classList.toggle('is-open');
      menu.setAttribute('aria-expanded', String(open));
      menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    });
    links.addEventListener('click', (event) => {
      if (event.target.closest('a')) {
        links.classList.remove('is-open');
        menu.setAttribute('aria-expanded', 'false');
        menu.setAttribute('aria-label', 'Open navigation');
      }
    });
  }

  const chartCanvas = document.querySelector('#paper-results-canvas');
  const splitSelect = document.querySelector('#paper-results-split');
  const metricSelect = document.querySelector('#paper-results-metric');
  const directionBadge = document.querySelector('#paper-results-direction');
  const status = document.querySelector('#paper-results-status');
  const topFiveList = document.querySelector('#paper-results-top-five');
  if (!chartCanvas || !splitSelect || !metricSelect || !directionBadge || !status || !topFiveList) return;

  const colors = [
    '#46504c', '#6f8f83', '#94ada3', '#bdcbc4', '#667c9e',
    '#96a7c4', '#90819d', '#b39aa7', '#b18d72', '#c5b482'
  ];

  const formatValue = (value) => {
    const absolute = Math.abs(value);
    if ((absolute > 0 && absolute < 0.001) || absolute >= 1000) return value.toExponential(3);
    return new Intl.NumberFormat('en-US', { maximumSignificantDigits: 5 }).format(value);
  };

  const addOptions = (data) => {
    data.splits.forEach((split) => splitSelect.add(new Option(split.label, split.id)));
    const families = [
      ['mechanism', 'Mechanism fidelity'],
      ['similarity', 'Traditional similarity']
    ];
    families.forEach(([family, label]) => {
      const group = document.createElement('optgroup');
      group.label = label;
      data.metrics.filter((metric) => metric.family === family).forEach((metric) => {
        group.append(new Option(metric.label, metric.id));
      });
      metricSelect.append(group);
    });
  };

  const getScaleType = (data, metric) => {
    const metricResults = data.results[splitSelect.value][metric.id];
    const values = data.representations.flatMap((representation) =>
      data.models.map((model) => metricResults[representation.id][model])
    ).filter((value) => value !== null && value > 0);
    const hasNonPositive = data.representations.some((representation) =>
      data.models.some((model) => {
        const value = metricResults[representation.id][model];
        return value !== null && value <= 0;
      })
    );
    return !hasNonPositive && Math.max(...values) / Math.min(...values) > 100 ? 'logarithmic' : 'linear';
  };

  const rankCombinations = (data, metric, metricResults) => {
    const combinations = data.representations.flatMap((representation, datasetIndex) =>
      data.models.map((model, modelIndex) => ({
        model,
        modelIndex,
        representation: representation.label,
        datasetIndex,
        value: metricResults[representation.id][model]
      }))
    ).filter((item) => item.value !== null);
    const score = metric.direction === 'target-one'
      ? (value) => Math.abs(value - 1)
      : metric.direction === 'higher' ? (value) => -value : (value) => value;
    return combinations.sort((left, right) => score(left.value) - score(right.value)).slice(0, 5);
  };

  const renderTopFive = (topFive) => {
    topFiveList.replaceChildren(...topFive.map((item) => {
      const entry = document.createElement('li');
      const combination = document.createElement('strong');
      const value = document.createElement('em');
      combination.textContent = `${item.model} / ${item.representation}`;
      value.textContent = formatValue(item.value);
      entry.append(combination, value);
      return entry;
    }));
  };

  const topFiveMedalsPlugin = {
    id: 'topFiveMedals',
    afterDatasetsDraw(chart) {
      const context = chart.ctx;
      context.save();
      const medalColors = [
        { fill: '#d4a72c', stroke: '#9a6b0b' },
        { fill: '#aeb8c1', stroke: '#6f7c87' },
        { fill: '#b77b55', stroke: '#7e4d34' }
      ];
      (chart.$topFive || []).slice(0, 3).forEach((item, rank) => {
        const bar = chart.getDatasetMeta(item.datasetIndex).data[item.modelIndex];
        if (!bar) return;
        const centerY = Math.max(chart.chartArea.top + 10, bar.y - 9);
        context.fillStyle = '#0d7757';
        context.beginPath();
        context.moveTo(bar.x - 3.5, centerY - 7);
        context.lineTo(bar.x - .5, centerY - 2);
        context.lineTo(bar.x - 4.5, centerY + 1);
        context.closePath();
        context.fill();
        context.beginPath();
        context.moveTo(bar.x + 3.5, centerY - 7);
        context.lineTo(bar.x + .5, centerY - 2);
        context.lineTo(bar.x + 4.5, centerY + 1);
        context.closePath();
        context.fill();
        context.beginPath();
        context.arc(bar.x, centerY + 2, 4.5, 0, Math.PI * 2);
        context.fillStyle = medalColors[rank].fill;
        context.fill();
        context.lineWidth = 1;
        context.strokeStyle = medalColors[rank].stroke;
        context.stroke();
      });
      context.restore();
    }
  };

  const initializeResults = async () => {
    if (typeof Chart === 'undefined') throw new Error('Chart library unavailable');
    let data = window.SIMUCELLA_BENCHMARK_RESULTS;
    if (!data) {
      const response = await fetch('assets/benchmark-results.json');
      if (!response.ok) throw new Error(`Benchmark data request failed (${response.status})`);
      data = await response.json();
    }
    addOptions(data);
    splitSelect.value = 'iid-sample';
    metricSelect.value = 'atomic-pcs';

    const chart = new Chart(chartCanvas, {
      type: 'bar',
      plugins: [topFiveMedalsPlugin],
      data: { labels: data.models, datasets: [] },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 360 },
        interaction: { mode: 'index', intersect: false },
        layout: { padding: { top: 4 } },
        plugins: {
          legend: {
            position: 'top',
            align: 'start',
            labels: { boxWidth: 10, boxHeight: 10, padding: 15, color: '#42554d', font: { size: 11, weight: 600 } }
          },
          tooltip: {
            filter: (item) => item.raw !== null,
            callbacks: {
              title: (items) => items[0]?.label || '',
              label: (item) => {
                const rank = item.chart.$topFive?.findIndex((ranked) =>
                  ranked.datasetIndex === item.datasetIndex && ranked.modelIndex === item.dataIndex
                );
                return ` ${rank >= 0 ? `#${rank + 1}  ` : ''}${item.dataset.label}: ${formatValue(item.raw)}`;
              }
            }
          }
        },
        scales: {
          x: {
            stacked: false,
            grid: { display: false },
            border: { color: '#aab7b1' },
            ticks: {
              color: (context) => context.index < 3 ? '#a6463d' : '#24352e',
              callback: function(value, index) {
                const label = this.getLabelForValue(value);
                return index < 3 ? [label, '(baseline)'] : label;
              },
              maxRotation: 0,
              minRotation: 0,
              font: (context) => ({ size: context.index < 3 ? 11 : 12, weight: context.index < 3 ? 750 : 650 })
            }
          },
          y: {
            beginAtZero: true,
            grid: { color: '#e4eae7' },
            border: { display: false },
            ticks: { color: '#607069', font: { size: 11 }, callback: (value) => formatValue(value) },
            title: { display: true, color: '#24352e', font: { size: 12, weight: 650 } }
          }
        }
      }
    });

    const updateChart = () => {
      const split = data.splits.find((item) => item.id === splitSelect.value);
      const metric = data.metrics.find((item) => item.id === metricSelect.value);
      const metricResults = data.results[split.id][metric.id];
      const topFive = rankCombinations(data, metric, metricResults);
      chart.$topFive = topFive;
      chart.data.datasets = data.representations.map((representation, index) => ({
        label: representation.label,
        data: data.models.map((model) => metricResults[representation.id][model]),
        backgroundColor: colors[index],
        borderColor: colors[index],
        borderWidth: 0,
        borderRadius: 1,
        categoryPercentage: 0.84,
        barPercentage: 0.92,
        maxBarThickness: 10
      }));
      chart.options.scales.y.type = getScaleType(data, metric);
      chart.options.scales.y.beginAtZero = chart.options.scales.y.type === 'linear';
      chart.options.scales.y.title.text = `${metric.label}${chart.options.scales.y.type === 'logarithmic' ? ' (log scale)' : ''}`;
      directionBadge.dataset.direction = metric.direction;
      directionBadge.textContent = metric.direction === 'target-one'
        ? 'Closer to 1 is better'
        : `${metric.direction === 'higher' ? 'Higher' : 'Lower'} is better`;
      status.textContent = `${split.label} / ${metric.label} / mean of 3 runs`;
      renderTopFive(topFive);
      chartCanvas.setAttribute('aria-label', `${metric.label} benchmark results for ${split.label}, mean of three runs`);
      chart.update();
    };

    splitSelect.addEventListener('change', updateChart);
    metricSelect.addEventListener('change', updateChart);
    updateChart();
  };

  initializeResults().catch((error) => {
    status.textContent = 'Benchmark results could not be loaded.';
    status.dataset.error = 'true';
    console.error(error);
  });
})();
