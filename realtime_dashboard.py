import dash
from dash import dcc, html
import plotly.graph_objs as go
import paho.mqtt.client as mqtt
import json

# Setup Dash App
app = dash.Dash(__name__)

# MQTT Setup
data_store = {"temperature": 0, "humidity": 0, "light": 0, "distance": 0}

def on_message(client, userdata, msg):
    global data_store
    try:
        payload = json.loads(msg.payload.decode())
        data_store.update(payload)
    except Exception as e:
        print("Error parsing payload:", e)

client = mqtt.Client()
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.subscribe("lab/telemetry")
client.loop_start()

app.layout = html.Div([
    html.H1("Real-Time IoT Telemetry"),
    dcc.Interval(id="interval-component", interval=2000, n_intervals=0),
    html.Div(id="live-update-text")
])

@app.callback(
    dash.dependencies.Output("live-update-text", "children"),
    [dash.dependencies.Input("interval-component", "n_intervals")]
)
def update_metrics(n):
    return [
        html.P(f"Temperature: {data_store['temperature']} °C"),
        html.P(f"Humidity: {data_store['humidity']} %"),
        html.P(f"Light Intensity: {data_store['light']}"),
        html.P(f"Distance: {data_store['distance']} cm")
    ]

if __name__ == "__main__":
    app.run_server(debug=True)
