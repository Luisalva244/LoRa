from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from db import Database
from datetime import datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="../LoRa-1/static/"), name="static")
db = Database()  


class RootFormat:

    @app.get("/", response_class=HTMLResponse)
    def show_screen():
        html_content = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Página de Introducción</title>
            <link rel="stylesheet" href="/static/styles.css">
        </head>
        <body>
            <main>
                <!-- Sección 1: Introducción -->
                <section id="seccion-uno" class="seccion">
                    <h1>Aplicaciones de LoRa con IoT en la agricultura de precisión.</h1>                   
                </section>

                <!-- Sección 2:  -->
                <section id="seccion-dos" class="seccion">
                    <h2>Enfoque del proyecto</h2>
                    <div class="servicios">
                        <div class="servicio">
                            <p>Este proyecto se enfoca en la implementación de una red de sensores IoT 
                                basada en la tecnología LoRa específicamente para el monitoreo agrícola en 
                                Monterrey, Nuevo León. Se establecerán dispositivos con sensores en áreas de 
                                cultivo para recolectar datos clave como la humedad del suelo, temperatura y 
                                humedad del ambiente, con el fin de optimizar prácticas agrícolas. </p>
                        </div>
                    </div>

                <!-- Sección 3: Monitoreo -->
                <section id="seccion-tres" class="seccion">
                    <h2>Monitoreo de los Datos</h2>
                    <p>Los dispositivos LoRa enviarán su información, la cual se recopilará en una base de datos y será procesada en tiempo real sobre las condiciones del suelo y el ambiente, permitiendo a los agricultores tomar decisiones informadas sobre el riego. Los datos incluirán:</p>
                    <ul>
                        <li>Humedad del suelo</li>
                        <li>Temperatura ambiental</li>
                        <li>Humedad relativa del aire</li>
                    </ul>
                    <p>Estos datos serán procesados y mostrados en tiempo real, ayudando a mejorar la eficiencia de las actividades agrícolas y reduciendo el uso de recursos como el agua.</p>
                    <div class="Semanabutton">
                        <button onclick="window.location.href='http://192.168.1.74:8000/readings/day'">Lecturas del dia</button>
                        <button onclick="window.location.href='http://192.168.1.74:8000/readings/week'">Promedio de la semana</button>                    
                    </div>                      
                </section>
                </section>
            </main>
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
                        
                        const labels = nodeData.map(item => item.timestamp.substring(11,16));
                        // Use humidity as the data
                        const humidityData = nodeData.map(item => item.Humidity);
                        const soilHumidityData = nodeData.map(item => item.soilHumidity);
                        const temperatureData = nodeData.map(item => item.Temperature);
                                        

                        // Create a heading for each node
                        const heading = document.createElement('h2');
                        document.getElementById('chartsContainer').appendChild(heading);

                        // Create a new canvas element
                        const canvas = document.createElement('canvas');
                        // Optionally set an ID if you want to reference it later
                        canvas.width = 30;
                        canvas.height = 10;
                        document.getElementById('chartsContainer').appendChild(canvas);

                        // Build the chart for this node
                        const ctx = canvas.getContext('2d');
                        new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: labels,
                            datasets: [
                            {
                            label: `Nodo ${node}`,
                            borderColor: 'gray',
                            },
                            {
                            label: `Humedad ambiental`,
                            data: humidityData,
                            borderColor: 'blue',
                            fill: false
                            },
                            {
                            label: `Humedad del suelo`,
                            data: soilHumidityData,
                            borderColor: 'green',
                            fill: false
                            },
                            {
                            label: `Temperatura`,
                            data: temperatureData,
                            borderColor: 'red',
                            fill: false
                            }
                        ]
                        },
                        options: {
                            plugins: {
                                legend: {
                                    labels: {
                                        font: {
                                            size: 15 
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
                        const labels = nodeData.map(item => item.timestamp.substring(5,10));

                        // Use humidity as the data
                        const humidityData = nodeData.map(item => item.Humidity);
                        const soilHumidityData = nodeData.map(item => item.soilHumidity);
                        const temperatureData = nodeData.map(item => item.Temperature);

                        // Create a heading for each node
                        const heading = document.createElement('h2');
                        document.getElementById('chartsContainer').appendChild(heading);

                        // Create a new canvas element
                        const canvas = document.createElement('canvas');
                        // Optionally set an ID if you want to reference it later
                        canvas.id = `chart_node_${node}`;
                        canvas.width = 30;
                        canvas.height = 10;
                        document.getElementById('chartsContainer').appendChild(canvas);

                        // Build the chart for this node
                        const ctx = canvas.getContext('2d');
                        new Chart(ctx, {
                        type: 'line',
                        data:{
                            labels: labels,
                            datasets: [
                                {
                                label: `Nodo ${node}`,
                                borderColor: 'gray',
                                },
                                {
                                    label: `Humedad ambiental`,
                                    data: humidityData,
                                    borderColor: 'blue',
                                    fill: false
                                },
                                {
                                    label: `Humedad del suelo`,
                                    data: soilHumidityData,
                                    borderColor: 'green',
                                    fill: false
                                },
                                {
                                    label: `Temperatura`,
                                    data: temperatureData,
                                    borderColor: 'red',
                                    fill: false
                                }
                            ]
                        },
                        options: {
                            plugins: {
                                legend: {
                                    labels: {
                                        font: {
                                            size: 15 
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
def read_readings_week():
    data = db.get_all_readings()

    # Get current week number (assumed to be the first two characters of the timestamp)
    date = datetime.now().strftime("%W %Y-%m-%d")
    current_week = date[0:2]
    
    # Filter readings from the current week
    week_readings = [reading for reading in data if reading["timestamp"][0:2] == current_week]
    week_readings = sorted(week_readings, key=lambda x: x["timestamp"][3:13])
    
    
    node_day_readings = {}
    for reading in week_readings:
        node = reading["node"]
        day = reading["timestamp"][3:13]  # e.g., "2025-04-03"
        if node not in node_day_readings:
            node_day_readings[node] = {}
        if day not in node_day_readings[node]:
    
            node_day_readings[node][day] = [node, 0, 0, 0, 0]
        
        node_day_readings[node][day][1] += reading["Humidity"]
        node_day_readings[node][day][2] += reading["soilHumidity"]
        node_day_readings[node][day][3] += reading["Temperature"]
        node_day_readings[node][day][4] += 1

    
    node_day_averages = []
    for node, days in node_day_readings.items():
        for day, values in days.items():
            _, hum_sum, soil_sum, temp_sum, count = values
            if count > 0:
                avg_humidity = round(hum_sum / count, 2)
                avg_soilHumidity = round(soil_sum / count, 2)
                avg_temperature = round(temp_sum / count, 2)
            else:
                avg_humidity = avg_soilHumidity = avg_temperature = 0
            node_day_averages.append({
                "node": node,
                "timestamp": day,  # The day of the reading
                "Humidity": avg_humidity,
                "soilHumidity": avg_soilHumidity,
                "Temperature": avg_temperature
            })

    print(node_day_averages)
    return sorted(node_day_averages, key=lambda x: (x["node"], x["timestamp"]))

@app.get("/readingsperday")
def read_readings():

  data = db.get_all_readings()
  
  date = datetime.now().strftime("%W %Y-%m-%d %H:%M")  # p.ej. "06 2025-04-03 15:00"
  today = date.strip()[3:13]
  today_readings = [reading for reading in data if reading["timestamp"][3:13] == today]
  today_readings = sorted(today_readings, key=lambda x: x["timestamp"]) 
  node_hour_readings = {}


  for reading in today_readings:
    node = reading["node"]
    hour = int(reading["timestamp"][14:16])

    if node not in node_hour_readings:
        node_hour_readings[node] = [[0, 0, 0, 0, 0] for _ in range(24)]  # [node, humidity_sum, soilHumidity_sum, temperature_sum, counter]


    humidity = reading["Humidity"]
    soilHumidity = reading["soilHumidity"]
    temperature = reading["Temperature"]

    
    node_hour_readings[node][hour][0] = node  
    node_hour_readings[node][hour][1] += humidity  
    node_hour_readings[node][hour][2] += soilHumidity  
    node_hour_readings[node][hour][3] += temperature  
    node_hour_readings[node][hour][4] += 1
             
  node_hour_averages = []
    
  for node, hours in node_hour_readings.items():
      for hour in range(24):  
        hour_data = hours[hour]
        if hour_data[4] > 0:  
            avg_humidity = round(hour_data[1] / hour_data[4],2)
            avg_soilHumidity = round(hour_data[2] / hour_data[4],2)
            avg_temperature = round(hour_data[3] / hour_data[4],2)
        else:
            avg_humidity = avg_soilHumidity = avg_temperature = 0

        timestamp = f"{today} {hour:02d}:00"  # Por ejemplo: "2025-04-03 14:00"

            # Añadimos los resultados de los promedios en el diccionario
        node_hour_averages.append({
            "node": node,
            "timestamp": timestamp,  # El timestamp generado
            "Humidity": avg_humidity,
            "soilHumidity": avg_soilHumidity,
            "Temperature": avg_temperature
        })

  print(node_hour_averages)  
  
  return node_hour_averages


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




@app.get("/weeks", response_class=HTMLResponse)
def show_weeks():
    data = db.get_all_readings()
    semanas = set()
    for lectura in data:
        # Se asume que los dos primeros caracteres del timestamp representan la semana
        semana = lectura["timestamp"][:2]
        semanas.add(semana)
    semanas = sorted(semanas)

    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Semanas Disponibles</title>
        <link rel="stylesheet" href="/static/styles.css">
    </head>
    <body>
        <header>
            <h1>Semanas disponibles en la base de datos</h1>
        </header>
        <main>
            <ul>
    """
    for s in semanas:
        # Al hacer clic se asume que se redirige a /readings/week con un query parameter
        html_content += f"<li><a href='/readings/week?week={s}'>Semana {s}</a></li>"
    html_content += """
            </ul>
        </main>
    </body>
    </html>
    """
    return html_content


if __name__ == "__main__":
    uvicorn.run("page:app", host="192.168.1.74", port=8000, reload=True)