

import dash
import dash_cytoscape as cyto
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'circle'},
        style={'width': '100%', 'height': '650px'},
        stylesheet=[
            {
                "selector": "node",
                "style": {
                    "label": "data(label)"
                }
            },
            {
                "selector": "edge",
                "style": {
                    "label": "data(weight)",
                    "curve-style": "bezier",
                    "target-arrow-shape": "triangle",
                }
            },
        ],
        elements=[
            # Node
            {
                "data": {"id": "db", "label": "DUBLIN"}
            },
            {
                "data": {"id": "ld", "label": "LONDON"}
            },
            {
                "data": {"id": "ny", "label": "NEW YORK"}
            },
            {
                "data": {"id": "hk", "label": "HONG KONG"}
            },
            {
                "data": {"id": "tk", "label": "TOKYO"}
            },
            {
                "data": {"id": "sg", "label": "SINGAPORE"}
            },
            {
                "data": {"id": "au", "label": "AUSTRALIA"}
            },
            {
                "data": {"id": "tr", "label": "TORONTO"}
            },

            # Edge
            {
                "data": {"id": "hk-ld", "source": "hk", "target": "ld", "weight": 210},
            },
            {
                "data": {"id": "ld-hk", "source": "ld", "target": "hk", "weight": 185},
            },
            {
                "data": {"id": "hk-ny", "source": "hk", "target": "ny", "weight": 235},
            },
            {
                "data": {"id": "ny-hk", "source": "ny", "target": "hk", "weight": 225},
            },
            {
                "data": {"id": "ld-ny", "source": "ld", "target": "ny", "weight": 235},
            },
            {
                "data": {"id": "ny-ld", "source": "ny", "target": "ld", "weight": 230},
            },
            {
                "data": {"id": "db-ld", "source": "db", "target": "ld", "weight": 150},
            },
            {
                "data": {"id": "ld-db", "source": "ld", "target": "db", "weight": 155},
            },
            {
                "data": {"id": "hk-tk", "source": "hk", "target": "tk", "weight": 120},
            },
            {
                "data": {"id": "tk-hk", "source": "tk", "target": "hk", "weight": 135},
            },
            {
                "data": {"id": "tk-sg", "source": "tk", "target": "sg", "weight": 25},
            },
            {
                "data": {"id": "sg-tk", "source": "sg", "target": "tk", "weight": 20},
            },
            {
                "data": {"id": "tk-hk", "source": "tk", "target": "hk", "weight": 135},
            },
            {
                "data": {"id": "au-sg", "source": "au", "target": "sg", "weight": 15},
            },
            {
                "data": {"id": "au-hk", "source": "au", "target": "hk", "weight": 25},
            },
            {
                "data": {"id": "tr-ny", "source": "tr", "target": "ny", "weight": 35},
            },
            {
                "data": {"id": "tr-ld", "source": "tr", "target": "ld", "weight": 30},
            },
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
