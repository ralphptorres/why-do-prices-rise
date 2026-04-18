const API_URL = 'http://localhost:8000/api';

let chart = null;
let pricesData = [];
let annotationsData = [];
let annotationsByDate = {};

async function fetchData() {
  try {
    const pricesRes = await fetch(`${API_URL}/prices`);
    const annotationsRes = await fetch(`${API_URL}/annotations`);
    
    const pricesJson = await pricesRes.json();
    const annotationsJson = await annotationsRes.json();
    
    pricesData = pricesJson.prices.sort((a, b) => new Date(a.date) - new Date(b.date));
    annotationsData = annotationsJson.annotations;
    
    annotationsData.forEach(ann => {
      annotationsByDate[ann.date] = ann;
    });
    
    renderChart();
  } catch (error) {
    console.error('Error fetching data:', error);
    document.getElementById('chipsContainer').innerHTML = '<p class="placeholder">Error loading data from API</p>';
  }
}

function renderChart() {
  if (pricesData.length === 0) return;
  
  const ctx = document.getElementById('priceChart').getContext('2d');

  const labels = pricesData.map(p => p.date);
  const prices = pricesData.map(p => p.prices.unleaded);
  
  const eventDates = annotationsData.map(a => a.date);
  const eventIndices = eventDates.map(date => labels.indexOf(date));

  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Gas Price (PHP/liter)',
          data: prices,
          borderColor: '#000000',
          backgroundColor: 'rgba(0, 0, 0, 0.05)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointRadius: 6,
          pointBackgroundColor: prices.map((_, index) =>
            eventIndices.includes(index) ? '#ff0000' : '#000000'
          ),
          pointBorderColor: prices.map((_, index) =>
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
              return `Price: P${context.parsed.y.toFixed(2)}/liter`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          ticks: {
            callback: (value) => `P${value}`
          }
        }
      },
      onHover: (event, activeElements) => {
        if (activeElements.length > 0) {
          const index = activeElements[0].index;
          const date = labels[index];
          displayChip(date);
        } else {
          clearChips();
        }
      }
    }
  });
}

function displayChip(date) {
  const annotation = annotationsByDate[date];
  const container = document.getElementById('chipsContainer');

  if (!annotation) {
    container.innerHTML = '<p class="placeholder">no events recorded for this date</p>';
    return;
  }

  const linksHtml = annotation.sources
    .map(source => `<a href="${source.url}" target="_blank" class="chip-link">${source.name}</a>`)
    .join('');

  const chipHtml = `
    <div class="chip">
      <div class="chip-date">${date}</div>
      <div class="chip-title">${annotation.event_title}</div>
      <div class="chip-description">${annotation.summary}</div>
      <div class="chip-links">${linksHtml}</div>
      <div class="chip-impact" style="font-size: 0.75rem; margin-top: 8px; color: #e74c3c; font-weight: 600;">${annotation.price_impact}</div>
    </div>
  `;

  container.innerHTML = chipHtml;
}

function clearChips() {
  const container = document.getElementById('chipsContainer');
  container.innerHTML = '<p class="placeholder">hover over data points to see related events</p>';
}

document.addEventListener('DOMContentLoaded', () => {
  fetchData();
});
