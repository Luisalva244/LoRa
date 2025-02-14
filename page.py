from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
from db import Database
from pageFormat import RootFormat


app = FastAPI()
db = Database()  

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
            <canvas id="myChart" width="100" height="50"></canvas>

            <script>
            // On page load, fetch your data from a /readings endpoint
            fetch('/readings')
            .then(response => response.json())
            .then(data => {

                
                // Extract labels (e.g., node or timestamp) and values (humidity)
                const labels = data.map(item => 'Node ' + item.id);
                const values = data.map(item => item.humidity);

                const ctx = document.getElementById('myChart').getContext('2d');

                new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                    label: 'Humidity',
                    data: values,
                    borderColor: 'red',
                    fill: true
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


class Reading(BaseModel):
    node: int
    humidity: float


@app.get("/")
def read_root():
    return RootFormat.show_chart()


@app.get("/readings")
def read_readings():
    return db.get_all_readings()

@app.post("/readings")
def create_reading(reading: Reading):
    db.writeData({
        "node": reading.node,
        "humidity": reading.humidity
    })
    return {
        "message": "Lectura insertada con éxito",
        "data": reading
    }

if __name__ == "__main__":
    uvicorn.run("page:app", host="127.0.0.1", port=8000, reload=True)