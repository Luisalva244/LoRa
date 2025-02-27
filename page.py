from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from db import Database
from datetime import datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="../GitHub/LoRa/static"), name="static")
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
            <link rel="stylesheet" type="text/css" href="/static/styles.css">
        </head>
        <body>
        <div>
        <img src="/static/fime.png" alt="HTML5 Icon" width="350" height="200" align="left" />
        <img src="/static/uanl.jpeg" alt="HTML5 Icon" width="350" height="200" align="right" />
        </div>
        <h2><button onclick="window.location.href='http://192.168.1.74:8000/readings/day'">Lecturas por dia</button></h2>
        </body>
        </html>
        """    
        return html_content


class ChartFormat:
    @app.get("/readings/day", response_class=HTMLResponse)
    def show_daychart():
       ## TO DO - Implement logic to display average values per hour of the day and new information (Temperature, Soil Humidity)
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Charts by Node</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <link rel="stylesheet" type="text/css" href="/static/styles.css">
        </head>
        <body>
            <h1>Humedad de los nodos en el dia</h1>
            <div class="button-container">    
                <div class="Iniciobutton">
                    <button onclick="window.location.href='http://192.168.1.74:8000/'">Inicio</button>
                </div>
                <div class="Semanabutton">
                    <button onclick="window.location.href='http://192.168.1.74:8000/readings/week'">Promedio de la semana</button>
                </div>
            </div>
            <!-- This container will hold multiple canvases, one per node. -->
            <div id="chartsContainer"></div>            
                <script>
                // Fetch data from /readings
                fetch('/readingsperday')
                    .then(response => response.json())
                    .then(data => {
                    // 1) Extract the unique node numbers
                    const uniqueNodes = [...new Set(data.map(item => item.node))];

                    // 2) For each node, filter the readings that belong to it
                    uniqueNodes.forEach(node => {
                        const nodeData = data.filter(item => item.node === node);
                        
                        const labels = nodeData.map(item => item.timestamp.substring(3,13));
                        // Use humidity as the data
                        const values = nodeData.map(item => item.Humidity);

                        // Create a heading for each node
                        const heading = document.createElement('h2');
                        document.getElementById('chartsContainer').appendChild(heading);

                        // Create a new canvas element
                        const canvas = document.createElement('canvas');
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
                            label: `Nodo ${node}`,
                            data: values,
                            borderColor: 'blue',
                            fill: false
                            }]
                        },
                        options: {
                            plugins: {
                                legend: {
                                    labels: {
                                        font: {
                                            size: 20 
                                        }
                                    }
                                }
                            },
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
            ## TO DO - Implement logic to display new information (Temperature, Soil Humidity)
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Charts by Node</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <link rel="stylesheet" type="text/css" href="/static/styles.css">
            </head>
            <body>
                <h1>Humedad de los nodos en la semana</h1>
                <div class="button-container">    
                    <div class="Iniciobutton">
                        <button onclick="window.location.href='http://192.168.1.74:8000/'">Inicio</button>
                    </div>
                    <div class="Semanabutton">
                        <button onclick="window.location.href='http://192.168.1.74:8000/readings/day'">Lecturas del dia</button>
                    </div>
                </div>    
                <!-- This container will hold multiple canvases, one per node. -->
                <div id="chartsContainer"></div>

                <script>
                // Fetch your data from /readings
                fetch('/readingsperweek')
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
                        const values = nodeData.map(item => item.Humidity);

                        // Create a heading for each node
                        const heading = document.createElement('h2');
                        document.getElementById('chartsContainer').appendChild(heading);

                        // Create a new canvas element
                        const canvas = document.createElement('canvas');
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
                            label: `Nodo ${node}`,
                            data: values,
                            borderColor: 'blue',
                            }]
                        },
                        options: {
                            plugins: {
                                legend: {
                                    labels: {
                                        font: {
                                            size: 20 
                                        }
                                    }
                                }
                            },
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

@app.get("/readingsperweek")
def read_readings():
    
  data = db.get_all_readings()

  date = datetime.now().strftime("%W %Y-%m-%d")
  week = date[0:2]
  week = [reading for reading in data if reading["timestamp"][0:2] == week]
  sorted_days = sorted(week, key=lambda x: x["timestamp"][3:13])
  totalHumidity_Per_DayNode = []

  for node in sorted_days:
    nodeNumber = node["node"]
    day = node["timestamp"][3:13]
    totalHumidityPerDay = 0  
    counter = 0

    for totalHumidity in sorted_days:
        if totalHumidity["node"] == nodeNumber and totalHumidity["timestamp"][3:13] == day: 
            totalHumidityPerDay += totalHumidity["Humidity"]
            if totalHumidityPerDay != 0:
                counter += 1     
    totalHumidity_Per_DayNode.append({"node": nodeNumber,"Humidity": round(totalHumidityPerDay/counter,2) , "timestamp": day})


  unique_totalHumidity_Per_DayNode = []
  seen = set()
  for item in totalHumidity_Per_DayNode:
    identifier = (item["node"], item["timestamp"])
    if identifier not in seen:
        unique_totalHumidity_Per_DayNode.append(item)
        seen.add(identifier)

  print(unique_totalHumidity_Per_DayNode)
            

  
  print(sorted_days)
  return sorted(unique_totalHumidity_Per_DayNode, key=lambda x: x["node"])


@app.get("/readingsperday")
def read_readings():

  data = db.get_all_readings()
  
  date = datetime.now().strftime("%W %Y-%m-%d")  # p.ej. "06 2025-04-03"
  today = date.strip()[3:13]
  today_readings = [reading for reading in data if reading["timestamp"][3:13] == today]
  print(data)

  return data


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
    uvicorn.run("page:app", host="192.168.1.74", port=8000, reload=True)