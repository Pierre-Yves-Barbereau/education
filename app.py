#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 16:41:21 2025

@author: pierre
"""

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
    html.Label('Valeur de r', style={'fontSize': '24px'}),
    html.Div([  # Wrap slider in Div for styling
        dcc.Slider(
            id='r-slider',
            min=-100000,
            max=100000,
            value=1,
            step=10000,
            marks={i: str(i) for i in range(-10, 11, 5)}
        )
    ], style={'width': '300px', 'margin': 'auto'}),
    html.Label('Valeur de p', style={'fontSize': '24px'}),
    html.Div([  # Wrap slider in Div for styling
        dcc.Slider(
            id='p-slider',
            min=2000,
            max=2025,
            value=2010,
            step=1,
            marks={i: str(i) for i in range(2000, 2026, 5)}
        )
    ], style={'width': '300px', 'margin': 'auto'}),
    html.Label('Valeur de u_p', style={'fontSize': '24px'}),
    html.Div([  # Wrap slider in Div for styling
        dcc.Slider(
            id='up-slider',
            min=-100000,
            max=100000,
            value=0,
            step=1000,
            marks={i: f'{i//1000}k' for i in range(-100000, 100001, 25000)}
        )
    ], style={'width': '300px', 'margin': 'auto'}),
    html.Label('Valeur de n_0', style={'fontSize': '24px'}),
    html.Div([  # Wrap slider in Div for styling
        dcc.Slider(
            id='n0-slider',
            min=2000,
            max=2025,
            value=2000,
            step=1,
            marks={i: str(i) for i in range(2000, 2026, 5)}
        )
    ], style={'width': '300px', 'margin': 'auto'})
], style={'textAlign': 'center', 'padding': '20px', 'maxWidth': '800px', 'margin': 'auto'})

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
    n = np.arange(2000, 2026)
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
        xaxis_range=[2000, 2025],
        yaxis_range=[-100000, 100000]
    )
    
    # Dynamic function display
    function_str = f'u_n = {r:.1f}(n - {p:.1f}) + {up:.1f}'
    
    return fig, function_str


# Expose the server for deployment (e.g., with Gunicorn)
server = app.server