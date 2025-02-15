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
    def show_screen():
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Charts by Node</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <h1>Bienvenido</h1>
            <h2><button onclick="window.location.href='http://127.0.0.1:8000/readings/day'">Lecturas por dia</button></h2>
        """    
        return html_content


class ChartFormat:
    @app.get("/readings/day", response_class=HTMLResponse)
    def show_daychart():
       ## TO DO - Implement space between the buttons and how to make smaller the charts  
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Charts by Node</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <h1>Humedad en los nodos en el dia</h1>
            <h2><button onclick="window.location.href='http://0.0.0.0:8000/'">Inicio</button><button onclick="window.location.href='http://0.0.0.0:8000/readings/week'">Promedio por semana</button></h2>
            <!-- This container will hold multiple canvases, one per node. -->
            <div id="chartsContainer"></div>

            <script>
            // Fetch your data from /readings
            fetch('/readings')
                .then(response => response.json())
                .then(data => {
                // 1) Extract the unique node numbers
                const uniqueNodes = [...new Set(data.map(item => item.node))];

                // 2) For each node, filter the readings that belong to it
                uniqueNodes.forEach(node => {
                    const nodeData = data.filter(item => item.node === node);
                    
                    // For example, use timestamps as labels
                    const labels = nodeData.map(item => item.timestamp);
                    // Use humidity as the data
                    const values = nodeData.map(item => item.humidity);

                    // Create a heading for each node
                    const heading = document.createElement('h2');
                    heading.textContent = `Nodo ${node}`;
                    document.getElementById('chartsContainer').appendChild(heading);

                    // Create a new canvas element
                    const canvas = document.createElement('canvas');
                    canvas.width = 300;
                    canvas.height = 150; 
                    // Optionally set an ID if you want to reference it later
                    // canvas.id = `chart_node_${node}`;
                    document.getElementById('chartsContainer').appendChild(canvas);

                    // Build the chart for this node
                    const ctx = canvas.getContext('2d');
                    new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                        label: `Humedad en nodo: ${node}`,
                        data: values,
                        borderColor: 'blue',
                        fill: false
                        }]
                    },
                    options: {
                        scales: {
                        y: {
                            beginAtZero: true
                        }
                        }
                    }
                    });
                });
                })
                .catch(err => console.error('Error fetching /readings:', err));
            </script>
        </body>
        </html>
        """

        return html_content

    @app.get("/readings/week", response_class=HTMLResponse)
    def show_weekchart():
            ## TO DO - Implement logic to handle the week chart with average values per day 
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Charts by Node</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            </head>
            <body>
                <h1>Humedad de los nodos en la semana</h1>
                <h2><button onclick="window.location.href='http://0.0.0.0:8000/readings/day'">Lecturas por dia</button></h2>
                <!-- This container will hold multiple canvases, one per node. -->
                <div id="chartsContainer"></div>

                <script>
                // Fetch your data from /readings
                fetch('/readings')
                    .then(response => response.json())
                    .then(data => {
                    // 1) Extract the unique node numbers
                    const uniqueNodes = [...new Set(data.map(item => item.node))];

                    // 2) For each node, filter the readings that belong to it
                    uniqueNodes.forEach(node => {
                        const nodeData = data.filter(item => item.node === node);
                        
                        // For example, use timestamps as labels
                        const labels = nodeData.map(item => item.timestamp);
                        // Use humidity as the data
                        const values = nodeData.map(item => item.humidity);

                        // Create a heading for each node
                        const heading = document.createElement('h2');
                        heading.textContent = `Nodo ${node}`;
                        document.getElementById('chartsContainer').appendChild(heading);

                        // Create a new canvas element
                        const canvas = document.createElement('canvas');
                        canvas.width = 300;
                        canvas.height = 150; 
                        // Optionally set an ID if you want to reference it later
                        // canvas.id = `chart_node_${node}`;
                        document.getElementById('chartsContainer').appendChild(canvas);

                        // Build the chart for this node
                        const ctx = canvas.getContext('2d');
                        new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: labels,
                            datasets: [{
                            label: `Humedad en nodo: ${node}`,
                            data: values,
                            borderColor: 'blue',
                            fill: false
                            }]
                        },
                        options: {
                            scales: {
                            y: {
                                beginAtZero: true
                            }
                            }
                        }
                        });
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
    return RootFormat.show_screen()


@app.get("/readings/day")
def read_root():
    return ChartFormat.show_daychart()

@app.get("/readings")
def read_readings():
   # db.get_all_readings()
    return [
  {"node":1,"humidity":55.0,"timestamp":"2025-01-01 10:00:00"},
  {"node":1,"humidity":55.1,"timestamp":"2025-01-01 10:01:00"},
  {"node":1,"humidity":55.2,"timestamp":"2025-01-01 10:02:00"},
  {"node":1,"humidity":55.3,"timestamp":"2025-01-01 10:03:00"},
  {"node":1,"humidity":55.4,"timestamp":"2025-01-01 10:04:00"},
  {"node":1,"humidity":55.5,"timestamp":"2025-01-01 10:05:00"},
  {"node":1,"humidity":55.6,"timestamp":"2025-01-01 10:06:00"},
  {"node":1,"humidity":55.7,"timestamp":"2025-01-01 10:07:00"},
  {"node":1,"humidity":55.8,"timestamp":"2025-01-01 10:08:00"},
  {"node":1,"humidity":55.9,"timestamp":"2025-01-01 10:09:00"},
  {"node":1,"humidity":56.0,"timestamp":"2025-01-01 10:10:00"},
  {"node":1,"humidity":56.1,"timestamp":"2025-01-01 10:11:00"},
  {"node":1,"humidity":56.2,"timestamp":"2025-01-01 10:12:00"},
  {"node":1,"humidity":56.3,"timestamp":"2025-01-01 10:13:00"},
  {"node":1,"humidity":56.4,"timestamp":"2025-01-01 10:14:00"},
  {"node":1,"humidity":56.5,"timestamp":"2025-01-01 10:15:00"},
  {"node":1,"humidity":30,"timestamp":"2025-01-01 10:16:00"},
  {"node":1,"humidity":56.7,"timestamp":"2025-01-01 10:17:00"},
  {"node":1,"humidity":56.8,"timestamp":"2025-01-01 10:18:00"},
  {"node":1,"humidity":56.9,"timestamp":"2025-01-01 10:19:00"},
  {"node":1,"humidity":57.0,"timestamp":"2025-01-01 10:20:00"},
  {"node":1,"humidity":57.1,"timestamp":"2025-01-01 10:21:00"},
  {"node":1,"humidity":57.2,"timestamp":"2025-01-01 10:22:00"},
  {"node":1,"humidity":57.3,"timestamp":"2025-01-01 10:23:00"},
  {"node":1,"humidity":57.4,"timestamp":"2025-01-01 10:24:00"},
  {"node":1,"humidity":57.5,"timestamp":"2025-01-01 10:25:00"},
  {"node":1,"humidity":57.6,"timestamp":"2025-01-01 10:26:00"},
  {"node":1,"humidity":57.7,"timestamp":"2025-01-01 10:27:00"},
  {"node":1,"humidity":57.8,"timestamp":"2025-01-01 10:28:00"},
  {"node":1,"humidity":57.9,"timestamp":"2025-01-01 10:29:00"},
  {"node":1,"humidity":58.0,"timestamp":"2025-01-01 10:30:00"},
  {"node":1,"humidity":58.1,"timestamp":"2025-01-01 10:31:00"},
  {"node":1,"humidity":58.2,"timestamp":"2025-01-01 10:32:00"},
  {"node":1,"humidity":58.3,"timestamp":"2025-01-01 10:33:00"},
  {"node":1,"humidity":58.4,"timestamp":"2025-01-01 10:34:00"},
  {"node":1,"humidity":58.5,"timestamp":"2025-01-01 10:35:00"},
  {"node":1,"humidity":58.6,"timestamp":"2025-01-01 10:36:00"},
  {"node":1,"humidity":58.7,"timestamp":"2025-01-01 10:37:00"},
  {"node":1,"humidity":58.8,"timestamp":"2025-01-01 10:38:00"},
  {"node":1,"humidity":58.9,"timestamp":"2025-01-01 10:39:00"},
  {"node":1,"humidity":59.0,"timestamp":"2025-01-01 10:40:00"},
  {"node":1,"humidity":59.1,"timestamp":"2025-01-01 10:41:00"},
  {"node":1,"humidity":59.2,"timestamp":"2025-01-01 10:42:00"},
  {"node":1,"humidity":59.3,"timestamp":"2025-01-01 10:43:00"},
  {"node":1,"humidity":59.4,"timestamp":"2025-01-01 10:44:00"},
  {"node":1,"humidity":59.5,"timestamp":"2025-01-01 10:45:00"},
  {"node":1,"humidity":59.6,"timestamp":"2025-01-01 10:46:00"},
  {"node":1,"humidity":59.7,"timestamp":"2025-01-01 10:47:00"},
  {"node":1,"humidity":59.8,"timestamp":"2025-01-01 10:48:00"},
  {"node":1,"humidity":59.9,"timestamp":"2025-01-01 10:49:00"},
  {"node":2,"humidity":65.0,"timestamp":"2025-01-01 10:00:00"},
  {"node":2,"humidity":65.1,"timestamp":"2025-01-01 10:01:00"},
  {"node":2,"humidity":65.2,"timestamp":"2025-01-01 10:02:00"},
  {"node":2,"humidity":65.3,"timestamp":"2025-01-01 10:03:00"},
  {"node":2,"humidity":65.4,"timestamp":"2025-01-01 10:04:00"},
  {"node":2,"humidity":65.5,"timestamp":"2025-01-01 10:05:00"},
  {"node":2,"humidity":65.6,"timestamp":"2025-01-01 10:06:00"},
  {"node":2,"humidity":65.7,"timestamp":"2025-01-01 10:07:00"},
  {"node":2,"humidity":65.8,"timestamp":"2025-01-01 10:08:00"},
  {"node":2,"humidity":65.9,"timestamp":"2025-01-01 10:09:00"},
  {"node":2,"humidity":66.0,"timestamp":"2025-01-01 10:10:00"},
  {"node":2,"humidity":66.1,"timestamp":"2025-01-01 10:11:00"},
  {"node":2,"humidity":66.2,"timestamp":"2025-01-01 10:12:00"},
  {"node":2,"humidity":66.3,"timestamp":"2025-01-01 10:13:00"},
  {"node":2,"humidity":66.4,"timestamp":"2025-01-01 10:14:00"},
  {"node":2,"humidity":66.5,"timestamp":"2025-01-01 10:15:00"},
  {"node":2,"humidity":66.6,"timestamp":"2025-01-01 10:16:00"},
  {"node":2,"humidity":66.7,"timestamp":"2025-01-01 10:17:00"},
  {"node":2,"humidity":66.8,"timestamp":"2025-01-01 10:18:00"},
  {"node":2,"humidity":66.9,"timestamp":"2025-01-01 10:19:00"},
  {"node":2,"humidity":67.0,"timestamp":"2025-01-01 10:20:00"},
  {"node":2,"humidity":67.1,"timestamp":"2025-01-01 10:21:00"},
  {"node":2,"humidity":67.2,"timestamp":"2025-01-01 10:22:00"},
  {"node":2,"humidity":67.3,"timestamp":"2025-01-01 10:23:00"},
  {"node":2,"humidity":67.4,"timestamp":"2025-01-01 10:24:00"},
  {"node":2,"humidity":67.5,"timestamp":"2025-01-01 10:25:00"},
  {"node":2,"humidity":67.6,"timestamp":"2025-01-01 10:26:00"},
  {"node":2,"humidity":67.7,"timestamp":"2025-01-01 10:27:00"},
  {"node":2,"humidity":67.8,"timestamp":"2025-01-01 10:28:00"},
  {"node":2,"humidity":67.9,"timestamp":"2025-01-01 10:29:00"},
  {"node":2,"humidity":68.0,"timestamp":"2025-01-01 10:30:00"},
  {"node":2,"humidity":68.1,"timestamp":"2025-01-01 10:31:00"},
  {"node":2,"humidity":68.2,"timestamp":"2025-01-01 10:32:00"},
  {"node":2,"humidity":68.3,"timestamp":"2025-01-01 10:33:00"},
  {"node":2,"humidity":68.4,"timestamp":"2025-01-01 10:34:00"},
  {"node":2,"humidity":68.5,"timestamp":"2025-01-01 10:35:00"},
  {"node":2,"humidity":68.6,"timestamp":"2025-01-01 10:36:00"},
  {"node":2,"humidity":68.7,"timestamp":"2025-01-01 10:37:00"},
  {"node":2,"humidity":68.8,"timestamp":"2025-01-01 10:38:00"},
  {"node":2,"humidity":68.9,"timestamp":"2025-01-01 10:39:00"},
  {"node":2,"humidity":69.0,"timestamp":"2025-01-01 10:40:00"},
  {"node":2,"humidity":69.1,"timestamp":"2025-01-01 10:41:00"},
  {"node":2,"humidity":69.2,"timestamp":"2025-01-01 10:42:00"},
  {"node":2,"humidity":69.3,"timestamp":"2025-01-01 10:43:00"},
  {"node":2,"humidity":20,"timestamp":"2025-01-01 10:44:00"},
  {"node":2,"humidity":69.5,"timestamp":"2025-01-01 10:45:00"},
  {"node":2,"humidity":69.6,"timestamp":"2025-01-01 10:46:00"},
  {"node":2,"humidity":69.7,"timestamp":"2025-01-01 10:47:00"},
  {"node":2,"humidity":69.8,"timestamp":"2025-01-01 10:48:00"},
  {"node":2,"humidity":69.9,"timestamp":"2025-01-01 10:49:00"}
]


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



@app.get("/readings/week")
def read_readings_week():
    return ChartFormat.show_weekchart()


if __name__ == "__main__":
    uvicorn.run("page:app", host="0.0.0.0", port=8000, reload=True)