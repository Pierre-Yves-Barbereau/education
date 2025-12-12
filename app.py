#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 14:54:53 2025

@author: pierre
"""

import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Initialize the Dash app
app = Dash(__name__)

# Define the layout with the graph and sliders
app.layout = html.Div([
    html.H1(id='function-title', style={'fontSize': '50px', 'textAlign': 'center'}),
    dcc.Graph(id='interactive-graph', style={'height': '700px'}),
    html.Label('Valeur de a', style={'fontSize': '24px'}),
    html.Div([  # Wrap slider in Div for styling
        dcc.Slider(
            id='a-slider',
            min=-10,
            max=10,
            value=1,
            step=0.1,
            marks={i: str(i) for i in range(-10, 11, 5)}
        )
    ], style={'width': '300px', 'margin': 'auto'}),
    html.Label('Valeur de x_0', style={'fontSize': '24px'}),
    html.Div([  # Wrap slider in Div for styling
        dcc.Slider(
            id='alpha-slider',
            min=-10,
            max=10,
            value=0,
            step=0.1,
            marks={i: str(i) for i in range(-10, 11, 5)}
        )
    ], style={'width': '300px', 'margin': 'auto'}),
    html.Label('Valeur de b', style={'fontSize': '24px'}),
    html.Div([  # Wrap slider in Div for styling
        dcc.Slider(
            id='b-slider',
            min=-10,
            max=10,
            value=0,
            step=0.1,
            marks={i: str(i) for i in range(-10, 11, 5)}
        )
    ], style={'width': '300px', 'margin': 'auto'})
], style={'textAlign': 'center', 'padding': '20px', 'maxWidth': '800px', 'margin': 'auto'})

# Define the callback to update the graph and title based on slider values
@app.callback(
    [Output('interactive-graph', 'figure'),
     Output('function-title', 'children')],
    [Input('a-slider', 'value'),
     Input('alpha-slider', 'value'),
     Input('b-slider', 'value')]
)
def update_graph(a, x0, b):
    # Generate x values
    x = np.linspace(-10, 10, 100)
    # Compute y values based on the function
    y = a * (x - x0) + b
    
    # Create the figure without title
    fig = go.Figure()
    # Add the line
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Fonction'))
    # Add the red cross at (x0, b)
    fig.add_trace(go.Scatter(x=[x0], y=[b], mode='markers', 
                             marker=dict(color='red', symbol='x', size=15),
                             name='Point (x_0, b)'))
    
    fig.update_layout(
        xaxis_title='x',
        yaxis_title='y',
        yaxis_range=[-20, 20]  # Fixed y-range for better visualization
    )
    
    # Dynamic function display
    function_str = f'y = {a:.1f}(x - {x0:.1f}) + {b:.1f}'
    
    return fig, function_str

# Expose the server for deployment (e.g., with Gunicorn)
server = app.server