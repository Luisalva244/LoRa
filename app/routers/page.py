from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from app.routers.db import Database
from datetime import datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
db = Database()  

#TO DO: Move the HTML content to a separate file and load it here
#TO DO: Figure out how to run in parallel the Serial Communication and the FastAPI server usig threads 


#TO DO: After the previous points, add comments to the code, write in the readme how to run the project and access the web page  


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
                <section id="seccion-uno" class="seccion">
                    <h1 class="Header-Title"> Aplicaciones de LoRa con IoT en la agricultura de precisión</h1>                   
                </section>

                <section id="seccion-dos" class="seccion">
                <h2 class="Header-Subtitle">Enfoque del proyecto</h2>
                <div class="servicios">
                    <!-- Text content on the left -->
                    <div class="text-content">
                    <p class="Text-Body">
                        Este proyecto se enfoca en la implementación de una red de sensores IoT basada en la tecnología LoRa
                        específicamente para el monitoreo agrícola en Monterrey, Nuevo León. Se establecerán dispositivos
                        con sensores en áreas de cultivo para recolectar datos clave como la humedad del suelo, temperatura y
                        humedad del ambiente, con el fin de optimizar prácticas agrícolas.
                    </p>
                    </div>
                    <!-- Image on the right -->
                    <div class="image-container">
                    <img src="/static/LoRa (1).jpg" alt="LoRa">
                    </div>
                </div>
                </section>

                <section id="seccion-tres" class="seccion">
                    <h2 class="Header-Subtitle">Monitoreo de los Datos</h2>
                    <p class="Text-Body">Los dispositivos LoRa enviarán su información, la cual se recopilará en una base de datos y será procesada en tiempo real sobre las condiciones del suelo y el ambiente, permitiendo a los agricultores tomar decisiones informadas sobre el riego. Los datos incluirán:</p>
                    <br>
                        <li class="Text-Body">Humedad del suelo</li>
                        <li class="Text-Body">Temperatura ambiental</li>
                        <li class="Text-Body">Humedad relativa del aire</li>
                    <br>
                    <p class="Text-Body">Estos datos serán procesados y mostrados en tiempo real, ayudando a mejorar la eficiencia de las actividades agrícolas y reduciendo el uso de recursos como el agua.</p>
                    <br>
                    <div class="Graphbutton">
                        <button onclick="window.location.href='http://192.168.1.74:8000/readings/day'">Graficas</button>
                    </div>
                </section>
            </main>
        </body>
        </html>
        """
        return html_content


class ChartFormat:
    @app.get("/readings/day", response_class=HTMLResponse)
    def show_daychart():
        html_content = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
          <meta charset="UTF-8">
          <title>Gráficas</title>
          <link rel="stylesheet" type="text/css" href="/static/styles.css">
          <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
        <div class="controls-area">
        <h1 class="Header-Title-Graph" style="margin-bottom: 5px;">Informacion de los nodos</h1>
        <div class="button-container" style="display: flex; flex-wrap: nowrap; align-items: center; gap: 10px;">
            <!-- Botón "Inicio" -->
            <div class="Semanabutton" style="width: 200px; height: 30px;">
            <button onclick="window.location.href='http://192.168.1.74:8000/'" 
                    style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                Inicio
            </button>
            </div>
            <!-- Selector para escoger vista: día o semana -->
            <div class="Semanabutton" style="width: 200px; height: 30px;">
            <select id="chartSelect" style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; text-align-last: center;">
                <option value="day">Lecturas del día</option>
                <option value="week">Promedio de la semana</option>
            </select>
            </div>
            <!-- Control para "Selecciona un nodo" para lectura del día -->
            <div id="nodeSelectDayContainer" class="Semanabutton" style="width: 200px; height: 30px;">
            <select id="nodeSelectDay" 
                    style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; text-align-last: center;">
                <option value="">Selecciona un nodo</option>
            </select>
            </div>
            <!-- Control para "Selecciona un día" -->
            <div id="SelectDayContainer" class="Semanabutton" style="width: 200px; height: 30px;">
            <select id="SelectDay" 
                    style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; text-align-last: center;">
                <option value="">Selecciona un día</option>
            </select>
            </div>
            <!-- Control para "Selecciona un nodo" para lectura de la semana (oculto por defecto) -->
            <div id="nodeSelectWeekContainer" class="Semanabutton" style="width: 200px; height: 30px; display: none;">
            <select id="nodeSelectWeek" 
                    style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; text-align-last: center;">
                <option value="">Selecciona un nodo</option>
            </select>
            </div>
            <!-- Control para "Selecciona una semana" (oculto por defecto) -->
            <div id="SelectWeekContainer" class="Semanabutton" style="width: 200px; height: 30px; display: none;">
            <select id="SelectWeek" 
                    style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; text-align-last: center;">
                <option value="">Selecciona una semana</option>
            </select>
            </div>
        </div>
        </div>
          <!-- Contenedor para la gráfica -->
          <div id="chartsContainer">
            <canvas id="chartCanvas" width="400" height="800"></canvas>
          </div>
          <script>
            let chartInstance = null;

            // Función para actualizar la gráfica de lectura del día
            function updateDayChart(selectedNode, selectedDay) {
              let url = '/readingsperday';
              if (selectedDay) {
                url += '?date=' + selectedDay;
              }
              fetch(url)
                .then(response => response.json())
                .then(data => {
                  if (selectedNode) {
                    data = data.filter(item => item.node == selectedNode);
                  }
                  if (data.length === 0) return;
                  const labels = data.map(item => item.timestamp.substring(11, 16));
                  const humidity = data.map(item => item.Humidity);
                  const soilHumidity = data.map(item => item.soilHumidity);
                  const temperature = data.map(item => item.Temperature);
                  const ctx = document.getElementById("chartCanvas").getContext("2d");
                  if (chartInstance) {
                    chartInstance.destroy();
                  }
                  chartInstance = new Chart(ctx, {
                    type: 'line',
                    data: {
                      labels: labels,
                      datasets: [
                        { label: "Humedad ambiental", data: humidity, borderColor: 'blue', fill: false },
                        { label: "Humedad del suelo", data: soilHumidity, borderColor: 'green', fill: false },
                        { label: "Temperatura", data: temperature, borderColor: 'red', fill: false }
                      ]
                    },
                    options: {
                      plugins: { legend: { labels: { font: { size: 15 } } } },
                      scales: { y: { beginAtZero: true } },
                      maintainAspectRatio: false
                    }
                  });
                })
                .catch(err => console.error('Error fetching /readingsperday:', err));
            }

            // Función para actualizar la gráfica de lectura de la semana
            function updateWeekChart(selectedNode, selectedWeek) {
              let url = '/readingsperweek';
              if (selectedWeek) {
                url += '?week=' + selectedWeek;
              }
              fetch(url)
                .then(response => response.json())
                .then(data => {
                  if (selectedNode) {
                    data = data.filter(item => item.node == selectedNode);
                  }
                  if (data.length === 0) return;
                  const labels = data.map(item => item.timestamp);
                  const humidity = data.map(item => item.Humidity);
                  const soilHumidity = data.map(item => item.soilHumidity);
                  const temperature = data.map(item => item.Temperature);
                  const ctx = document.getElementById("chartCanvas").getContext("2d");
                  if (chartInstance) {
                    chartInstance.destroy();
                  }
                  chartInstance = new Chart(ctx, {
                    type: 'line',
                    data: {
                      labels: labels,
                      datasets: [
                        { label: "Humedad ambiental", data: humidity, borderColor: 'blue', fill: false },
                        { label: "Humedad del suelo", data: soilHumidity, borderColor: 'green', fill: false },
                        { label: "Temperatura", data: temperature, borderColor: 'red', fill: false }
                      ]
                    },
                    options: {
                      plugins: { legend: { labels: { font: { size: 15 } } } },
                      scales: { y: { beginAtZero: true } },
                      maintainAspectRatio: false
                    }
                  });
                })
                .catch(err => console.error('Error fetching /readingsperweek:', err));
            }

            // Función que actualiza la gráfica según la selección de vista
            function updateChart() {
            const chartType = document.getElementById("chartSelect").value;
            if (chartType === "day") {
                document.getElementById("nodeSelectDayContainer").style.display = "block";
                document.getElementById("SelectDayContainer").style.display = "block";
                document.getElementById("nodeSelectWeekContainer").style.display = "none";
                document.getElementById("SelectWeekContainer").style.display = "none";
                const selectedNode = document.getElementById("nodeSelectDay").value;
                const selectedDay = document.getElementById("SelectDay").value;
                updateDayChart(selectedNode, selectedDay);
            } else {
                document.getElementById("nodeSelectDayContainer").style.display = "none";
                document.getElementById("SelectDayContainer").style.display = "none";
                document.getElementById("nodeSelectWeekContainer").style.display = "block";
                document.getElementById("SelectWeekContainer").style.display = "block";
                const selectedNode = document.getElementById("nodeSelectWeek").value;
                const selectedWeek = document.getElementById("SelectWeek").value;
                updateWeekChart(selectedNode, selectedWeek);
            }
            }

            // Listeners para el cambio de la vista
            document.getElementById("chartSelect").addEventListener("change", updateChart);

            // Para los selectores de día
            document.getElementById("SelectDay").addEventListener("change", function () {
              updateChart();
              loadNodesDay();
            });
            document.getElementById("nodeSelectDay").addEventListener("change", updateChart);

            // Para los selectores de semana
            document.getElementById("SelectWeek").addEventListener("change", updateChart);
            document.getElementById("nodeSelectWeek").addEventListener("change", updateChart);

            // Carga los días disponibles y los nodos para el día actual
            function loadDays() {
              fetch('/daysdata')
                .then(response => response.json())
                .then(days => {
                  const selectDay = document.getElementById("SelectDay");
                  selectDay.innerHTML = '<option value=""> Selecciona un día </option>';
                  days.forEach(day => {
                    let option = document.createElement("option");
                    option.value = day;
                    option.text = day;
                    selectDay.appendChild(option);
                  });
                  if (days.length > 0) {
                    selectDay.value = days[0];
                    updateChart();
                    loadNodesDay();
                  }
                })
                .catch(err => console.error('Error fetching /daysdata:', err));
            }

            function loadNodesDay() {
              let url = '/readingsperday';
              let selectedDay = document.getElementById("SelectDay").value;
              if (selectedDay) {
                url += '?date=' + selectedDay;
              }
              fetch(url)
                .then(response => response.json())
                .then(data => {
                  const nodes = [...new Set(data.map(item => item.node))];
                  const selectNode = document.getElementById("nodeSelectDay");
                  selectNode.innerHTML = '<option value=""> Selecciona un nodo </option>';
                  nodes.forEach(node => {
                    let option = document.createElement("option");
                    option.value = node;
                    option.text = "Nodo " + node;
                    selectNode.appendChild(option);
                  });
                })
                .catch(err => console.error('Error fetching nodes for day:', err));
            }

            // Carga las semanas disponibles y los nodos para la vista de semana
            function loadWeeks() {
              fetch('/weeksdata')
                .then(response => response.json())
                .then(weeks => {
                  const selectWeek = document.getElementById("SelectWeek");
                  selectWeek.innerHTML = '<option value=""> Selecciona una semana </option>';
                  weeks.forEach(week => {
                    let option = document.createElement("option");
                    option.value = week;
                    option.text = "Semana " + week;
                    selectWeek.appendChild(option);
                  });
                  if (weeks.length > 0) {
                    selectWeek.value = weeks[0];
                    updateChart();
                    loadNodesWeek();
                  }
                })
                .catch(err => console.error('Error fetching /weeksdata:', err));
            }

            function loadNodesWeek() {
              let url = '/readingsperweek';
              let selectedWeek = document.getElementById("SelectWeek").value;
              if (selectedWeek) {
                url += '?week=' + selectedWeek;
              }
              fetch(url)
                .then(response => response.json())
                .then(data => {
                  const nodes = [...new Set(data.map(item => item.node))];
                  const selectNode = document.getElementById("nodeSelectWeek");
                  selectNode.innerHTML = '<option value=""> Selecciona un nodo </option>';
                  nodes.forEach(node => {
                    let option = document.createElement("option");
                    option.value = node;
                    option.text = "Nodo " + node;
                    selectNode.appendChild(option);
                  });
                })
                .catch(err => console.error('Error fetching nodes for week:', err));
            }

            // Inicializa cargando ambos (días y semanas) y actualizando según la opción predeterminada
            loadDays();
            loadWeeks();
            updateChart();
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

@app.get("/daysdata")
def get_days_data():
    data = db.get_all_readings()

    current_month = datetime.now().strftime("%Y-%m")

    dias = { lectura["timestamp"][3:13] for lectura in data if lectura["timestamp"][3:10] == current_month }
    return sorted(dias)

@app.get("/readings/day")
def read_root():
    return ChartFormat.show_daychart()

@app.get("/readingsperday")
def read_readings(date: str = None):
    data = db.get_all_readings()
    
    if date:
        selected_day = date  
    else:
        now = datetime.now().strftime("%W %Y-%m-%d %H:%M")  # Ejemplo: "06 2025-04-03 15:00"
        selected_day = now[3:13]  
    
    today_readings = [reading for reading in data if reading["timestamp"][3:13] == selected_day]
    today_readings = sorted(today_readings, key=lambda x: x["timestamp"]) 
    node_hour_readings = {}

    for reading in today_readings:
        node = reading["node"]
        hour = int(reading["timestamp"][14:16])
        if node not in node_hour_readings:
            node_hour_readings[node] = [[0, 0, 0, 0, 0] for _ in range(24)]
        node_hour_readings[node][hour][0] = node  
        node_hour_readings[node][hour][1] += reading["Humidity"]  
        node_hour_readings[node][hour][2] += reading["soilHumidity"]  
        node_hour_readings[node][hour][3] += reading["Temperature"]  
        node_hour_readings[node][hour][4] += 1
             
    node_hour_averages = []
    for node, hours in node_hour_readings.items():
        for hour in range(24):
            hour_data = hours[hour]
            if hour_data[4] > 0:
                avg_humidity = round(hour_data[1] / hour_data[4], 2)
                avg_soilHumidity = round(hour_data[2] / hour_data[4], 2)
                avg_temperature = round(hour_data[3] / hour_data[4], 2)
            else:
                avg_humidity = avg_soilHumidity = avg_temperature = 0

            timestamp = f"{selected_day} {hour:02d}:00"
            node_hour_averages.append({
                "node": node,
                "timestamp": timestamp,
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

@app.get("/readingsperweek")
def read_readings_week(week: str = None):
    data = db.get_all_readings()
    if week:
        week_readings = [reading for reading in data if reading["timestamp"][:2] == week]
    else:
        date = datetime.now().strftime("%W %Y-%m-%d")
        current_week = date[0:2]
        week_readings = [reading for reading in data if reading["timestamp"][:2] == current_week]
    
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
    for nodo, dias in node_day_readings.items():
        for dia, valores in dias.items():
            _, hum_sum, soil_sum, temp_sum, count = valores
            if count > 0:
                avg_humidity = round(hum_sum / count, 2)
                avg_soilHumidity = round(soil_sum / count, 2)
                avg_temperature = round(temp_sum / count, 2)
            else:
                avg_humidity = avg_soilHumidity = avg_temperature = 0
            node_day_averages.append({
                "node": nodo,
                "timestamp": dia,
                "Humidity": avg_humidity,
                "soilHumidity": avg_soilHumidity,
                "Temperature": avg_temperature
            })

    print(node_day_averages)
    return sorted(node_day_averages, key=lambda x: (x["node"], x["timestamp"]))

@app.get("/weeksdata")
def get_weeks_data():
    data = db.get_all_readings()
    semanas = set()
    for lectura in data:
        semana = lectura["timestamp"][0:2]
        semanas.add(semana)
    return sorted(semanas)

@app.get("/readings/week", response_class=HTMLResponse)
def show_weekchart(week: str = None):
    data = db.get_all_readings()
    if week:
        week_readings = [r for r in data if r["timestamp"][:2] == week]
        print(week_readings)
    else:
        date = datetime.now().strftime("%W %Y-%m-%d")
        current_week = date[0:2]
        week_readings = [r for r in data if r["timestamp"][:2] == current_week]
        

    week_readings = sorted(week_readings, key=lambda x: x["timestamp"][3:13])
    
    node_day_readings = {}
    for lectura in week_readings:
        node = lectura["node"]
        dia = lectura["timestamp"][3:13]  # e.g., "2025-04-03"
        if node not in node_day_readings:
            node_day_readings[node] = {}
        if dia not in node_day_readings[node]:
            node_day_readings[node][dia] = [node, 0, 0, 0, 0]
        node_day_readings[node][dia][1] += lectura["Humidity"]
        node_day_readings[node][dia][2] += lectura["soilHumidity"]
        node_day_readings[node][dia][3] += lectura["Temperature"]
        node_day_readings[node][dia][4] += 1

    node_day_averages = []
    for nodo, dias in node_day_readings.items():
        for dia, valores in dias.items():
            _, hum_sum, soil_sum, temp_sum, count = valores
            if count > 0:
                avg_humidity = round(hum_sum / count, 2)
                avg_soilHumidity = round(soil_sum / count, 2)
                avg_temperature = round(temp_sum / count, 2)
            else:
                avg_humidity = avg_soilHumidity = avg_temperature = 0
            node_day_averages.append({
                "node": nodo,
                "timestamp": dia,
                "Humidity": avg_humidity,
                "soilHumidity": avg_soilHumidity,
                "Temperature": avg_temperature
            })

    print(node_day_averages)
    return sorted(node_day_averages, key=lambda x: (x["node"], x["timestamp"]))

if __name__ == "__main__":
    uvicorn.run("app.routers.page:app", host="192.168.1.74", port=8000, reload=True)