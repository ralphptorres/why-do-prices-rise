let chart = null;

function renderChart() {
  const ctx = document.getElementById('priceChart').getContext('2d');

  const eventDates = Object.keys(priceData.events);
  const eventIndices = eventDates.map(date => priceData.labels.indexOf(date));

  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: priceData.labels,
      datasets: [
        {
          label: 'Gas Price (PHP/liter)',
          data: priceData.prices,
          borderColor: '#000000',
          backgroundColor: 'rgba(0, 0, 0, 0.05)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointRadius: 6,
          pointBackgroundColor: priceData.prices.map((_, index) =>
            eventIndices.includes(index) ? '#ff0000' : '#000000'
          ),
          pointBorderColor: priceData.prices.map((_, index) =>
            eventIndices.includes(index) ? '#cc0000' : '#000000'
          ),
          pointBorderWidth: 2,
          pointHoverRadius: 8,
          pointHoverBackgroundColor: '#ffcc00',
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          labels: {
            font: { size: 12 }
          }
        },
        tooltip: {
          enabled: true,
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleFont: { size: 13, weight: 'bold' },
          bodyFont: { size: 12 },
          padding: 12,
          cornerRadius: 6,
          callbacks: {
            title: (context) => {
              return `${context[0].label}`;
            },
            label: (context) => {
              return `Price: ₱${context.parsed.y.toFixed(2)}/liter`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          min: 55,
          max: 80,
          ticks: {
            callback: (value) => `₱${value}`
          }
        }
      },
      onHover: (event, activeElements) => {
        if (activeElements.length > 0) {
          const index = activeElements[0].index;
          const date = priceData.labels[index];
          displayChip(date);
        } else {
          clearChips();
        }
      }
    }
  });
}

function displayChip(date) {
  const event = priceData.events[date];
  const container = document.getElementById('chipsContainer');

  if (!event) {
    container.innerHTML = '<p class="placeholder">no events recorded for this date</p>';
    return;
  }

  const linksHtml = event.sources
    .map(source => `<a href="${source.url}" target="_blank" class="chip-link">${source.name}</a>`)
    .join('');

  const chipHtml = `
    <div class="chip">
      <div class="chip-date">${date}</div>
      <div class="chip-title">${event.title}</div>
      <div class="chip-description">${event.description}</div>
      <div class="chip-links">${linksHtml}</div>
      <div class="chip-impact" style="font-size: 0.75rem; margin-top: 8px; color: #e74c3c; font-weight: 600;">${event.price_impact}</div>
    </div>
  `;

  container.innerHTML = chipHtml;
}

function clearChips() {
  const container = document.getElementById('chipsContainer');
  container.innerHTML = '<p class="placeholder">hover over data points to see related events</p>';
}

// initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  renderChart();
});
