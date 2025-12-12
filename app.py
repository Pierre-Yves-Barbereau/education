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

# Define the layout with the graph on the left and sliders on the right
app.layout = html.Div([
    html.Div([
        dcc.Markdown(id='function-title', mathjax=True, style={'fontSize': '50px', 'textAlign': 'center'}),
        dcc.Graph(id='interactive-graph', style={'height': '700px'}),
    ], style={'flex': '3', 'padding': '20px'}),
    html.Div([
        html.Label('Valeur de r', style={'fontSize': '24px', 'textAlign': 'center'}),
        html.Div([
            dcc.Slider(
                id='r-slider',
                min=-10000,
                max=10000,
                value=0,
                step=1000,
                marks={i: f'{i//1000}k' for i in range(-100000, 100001, 25000)}
            )
        ], style={'width': '250px', 'margin': '10px auto'}),
        html.Label('Valeur de p', style={'fontSize': '24px', 'textAlign': 'center'}),
        html.Div([
            dcc.Slider(
                id='p-slider',
                min=2000,
                max=2025,
                value=2010,
                step=1,
                marks={i: str(i) for i in range(2000, 2026, 5)}
            )
        ], style={'width': '250px', 'margin': '10px auto'}),
        html.Label('Valeur de u_p', style={'fontSize': '24px', 'textAlign': 'center'}),
        html.Div([
            dcc.Slider(
                id='up-slider',
                min=-100000,
                max=100000,
                value=0,
                step=1000,
                marks={i: f'{i//1000}k' for i in range(-100000, 100001, 25000)}
            )
        ], style={'width': '250px', 'margin': '10px auto'}),
        html.Label('Valeur de n_0', style={'fontSize': '24px', 'textAlign': 'center'}),
        html.Div([
            dcc.Slider(
                id='n0-slider',
                min=2000,
                max=2025,
                value=2000,
                step=1,
                marks={i: str(i) for i in range(2000, 2026, 5)}
            )
        ], style={'width': '250px', 'margin': '10px auto'})
    ], style={'flex': '1', 'padding': '20px', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'flex-start'})
], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'stretch', 'maxWidth': '1200px', 'margin': 'auto', 'padding': '20px'})

# Callback to update p-slider min and value based on n0
@app.callback(
    [Output('p-slider', 'min'),
     Output('p-slider', 'value')],
    [Input('n0-slider', 'value'),
     Input('p-slider', 'value')]
)
def update_p_slider(n0, current_p):
    min_p = n0
    new_value = max(min_p, current_p)
    return min_p, new_value

# Define the callback to update the graph and title based on slider values
@app.callback(
    [Output('interactive-graph', 'figure'),
     Output('function-title', 'children')],
    [Input('r-slider', 'value'),
     Input('p-slider', 'value'),
     Input('up-slider', 'value'),
     Input('n0-slider', 'value')]
)
def update_graph(r, p, up, n0):
    # Generate n values
    n = np.arange(2000, 2051)
    # Compute u_n values based on the function
    un = r * (n - p) + up
    
    # Filter for n > n0
    mask = n > n0
    n_plot = n[mask]
    un_plot = un[mask]
    
    # Create the figure without title
    fig = go.Figure()
    # Add the points
    fig.add_trace(go.Scatter(x=n_plot, y=un_plot, mode='markers', name='Termes de la suite'))
    # Add the red cross at (p, up)
    fig.add_trace(go.Scatter(x=[p], y=[up], mode='markers', 
                             marker=dict(color='red', symbol='x', size=15),
                             name='Point (p, u_p)'))
    
    fig.update_layout(
        xaxis_title='n',
        yaxis_title='u_n',
        xaxis_range=[2000, 2050],
        yaxis_range=[-100000, 100000]
    )
    
    # Dynamic function display in LaTeX
    function_str = f'$$u_n = {r:g}(n - {p:g}) + {up:g}$$'
    
    return fig, function_str


# Expose the server for deployment (e.g., with Gunicorn)
server = app.server