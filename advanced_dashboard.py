import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import paho.mqtt.client as mqtt
import json
import collections

# Circular buffers for rolling real-time graphs
MAX_POINTS = 20
timestamps = collections.deque(maxlen=MAX_POINTS)
temp_vals = collections.deque(maxlen=MAX_POINTS)
hum_vals = collections.deque(maxlen=MAX_POINTS)
light_vals = collections.deque(maxlen=MAX_POINTS)
dist_vals = collections.deque(maxlen=MAX_POINTS)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        import datetime
        timestamps.append(datetime.datetime.now().strftime("%H:%M:%S"))
        temp_vals.append(payload.get("temperature", 0))
        hum_vals.append(payload.get("humidity", 0))
        light_vals.append(payload.get("light", 0))
        dist_vals.append(payload.get("distance", 0))
    except Exception as e:
        print("Error:", e)

client = mqtt.Client()
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.subscribe("lab/telemetry")
client.loop_start()

app = dash.Dash(__name__)

app.layout = html.Div(style={"backgroundColor": "#1e1e1e", "color": "#ffffff", "padding": "20px"}, children=[
    html.H1("Advanced IoT Telemetry Dashboard (Dark Theme)", style={"textAlign": "center"}),
    dcc.Interval(id="graph-update", interval=2000, n_intervals=0),
    dcc.Graph(id="live-graph"),
])

@app.callback(
    Output("live-graph", "figure"),
    [Input("graph-update", "n_intervals")]
)
def update_graph(n):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(timestamps), y=list(temp_vals), name="Temp (°C)", mode="lines+markers"))
    fig.add_trace(go.Scatter(x=list(timestamps), y=list(hum_vals), name="Humidity (%)", mode="lines+markers"))
    fig.add_trace(go.Scatter(x=list(timestamps), y=list(light_vals), name="Light", mode="lines+markers"))
    fig.add_trace(go.Scatter(x=list(timestamps), y=list(dist_vals), name="Distance (cm)", mode="lines+markers"))
    
    fig.update_layout(
        template="plotly_dark",
        title="Real-Time Multi-Metric Stream",
        xaxis_title="Time",
        yaxis_title="Values"
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
