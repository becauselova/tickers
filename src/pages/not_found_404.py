import dash
dash.register_page(__name__)
from dash import html

dash.register_page(__name__, path="/404")

layout = html.H1("Custom 404")