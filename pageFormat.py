from fastapi.responses import HTMLResponse
from fastapi import FastAPI

app = FastAPI()


class RootFormat:

    @app.get("/", response_class=HTMLResponse)
    def show_chart():
        # For simplicity, we embed everything in a single HTML string.
        # This includes a fetch to a hypothetical endpoint /readings
        # which returns JSON data. We then build a chart with Chart.js.

        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>My Simple Chart</title>
            <!-- Load Chart.js from a CDN -->
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <h1>Humidity Chart</h1>
            <canvas id="myChart" width="600" height="400"></canvas>

            <script>
            // On page load, fetch your data from a /readings endpoint
            fetch('/readings')
            .then(response => response.json())
            .then(data => {
                // Suppose data is something like:
                // [ { "node": 1, "humidity": 55.4, "timestamp": "..." }, ... ]
                
                // Extract labels (e.g., node or timestamp) and values (humidity)
                const labels = data.map(item => 'Node ' + item.node);
                const values = data.map(item => item.humidity);

                const ctx = document.getElementById('myChart').getContext('2d');

                new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                    label: 'Humidity',
                    data: values,
                    borderColor: 'blue',
                    fill: false
                    }]
                },
                options: {
                    scales: {
                    y: { beginAtZero: true }
                    }
                }
                });
            })
            .catch(err => console.error('Error fetching /readings:', err));
            </script>
        </body>
        </html>
        """

        return html_content