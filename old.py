import time
from dash import Dash, Input, Output, html, dcc, callback
from dash.long_callback import DiskcacheLongCallbackManager
import plotly.graph_objects as go

# Diskcache for non-production apps when developing locally
import diskcache
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

app = Dash(__name__, long_callback_manager=long_callback_manager)

app.layout = html.Div(
    [
        html.Div([html.P(id="paragraph_id_1", children=["Button 1 not clicked"])]),
        html.Div([html.P(id="paragraph_id_2", children=["Button 2 not clicked"])]),
        html.Button(id="button_id_1", children="Run Job!"),
        html.Button(id="button_id_2", children="Run Job!"),
        html.Button(id="cancel_button_id", children="Cancel Running Job!"),
    ]
)

@app.long_callback(
    output=Output("paragraph_id_1", "children"),
    inputs=Input("button_id_1", "n_clicks"),
    prevent_initial_call=True,
    running=[
        (Output("button_id_1", "disabled"), True, False),
    ],
    cancel=[Input("cancel_button_id", "n_clicks")],
)
def update_clicks(n_clicks):
    time.sleep(2.0)
    return [f"Clicked Button 1: {n_clicks} times"]

@app.long_callback(
    output=Output("paragraph_id_2", "children"),
    inputs=Input("button_id_2", "n_clicks"),
    prevent_initial_call=True,
    running=[
        (Output("button_id_2", "disabled"), True, False),
    ],
    cancel=[Input("cancel_button_id", "n_clicks")],
)
def update_clicks(n_clicks):
    time.sleep(2.0)
    return [f"Clicked Button 2: {n_clicks} times"]

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
