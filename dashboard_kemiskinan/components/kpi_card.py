"""
KPI Card Component — Light Professional Theme
White cards with colored icon boxes, values, and sparklines.
"""
from dash import html, dcc
import dash_bootstrap_components as dbc

from components.chart_utils import create_sparkline

# Icon box color mapping
ICON_COLORS = {
    'juta': ('teal', '#3d8b8a'),
    'persen': ('blue', '#4a8fa8'),
    'rupiah': ('amber', '#5ba4a4'),
    'desimal3': ('rose', '#7caec4'),
    'kota': ('green', '#80cbc4'),
    'desa': ('purple', '#9fc5d5'),
}


def create_kpi_card(card_id, label, value, yoy_change, sparkline_data,
                    icon, fmt='persen', is_critical=False, progress=50):
    """Create a single KPI card with light professional styling."""

    # Determine change direction
    if yoy_change < 0:
        change_text = f'▼ {abs(yoy_change):.1f}% dari tahun lalu'
        change_class = 'positive'  # Decrease in poverty = positive
    elif yoy_change > 0:
        change_text = f'▲ {yoy_change:.1f}% dari tahun lalu'
        change_class = 'negative'
    else:
        change_text = '— Tidak ada perubahan'
        change_class = 'positive'

    # Icon box color
    box_class, spark_color = ICON_COLORS.get(fmt, ('teal', '#4db6ac'))

    # Sparkline figure
    sparkline_fig = create_sparkline(sparkline_data, color=spark_color)

    # Glow class for critical
    card_classes = 'glass-card kpi-card gradient-border'
    if is_critical:
        card_classes += ' glow-danger'

    return dbc.Col([
        html.Div([
            # Label row with icon
            html.Div([
                html.Div(icon, className=f'kpi-icon-box {box_class}'),
                html.Span(label),
            ], className='kpi-label'),

            # Value
            html.Div(value, className='kpi-value', id=f'kpi-value-{card_id}'),

            # YoY Change
            html.Div(change_text, className=f'kpi-change {change_class}'),

            # Sparkline
            html.Div([
                dcc.Graph(
                    figure=sparkline_fig,
                    config={'displayModeBar': False},
                    style={'height': '30px'},
                ),
            ], className='kpi-sparkline'),

            # Progress bar
            html.Div([
                html.Div(style={'width': f'{progress:.0f}%'}, className='kpi-progress-fill'),
            ], className='kpi-progress-bar'),

        ], className=card_classes),
    ], lg=2, md=4, sm=6, xs=12)
