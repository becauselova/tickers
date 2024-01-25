import dash
import dash_bootstrap_components as dbc
import dash_auth

USERNAME_PASSWORD_PAIRS=[['username', 'password'], ['623', '63']]

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

server = app.server

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [dbc.DropdownMenuItem(page["name"], href=page["path"])
         for page in dash.page_registry.values()
         if page["module"]!="pages.not_found_404"
        ],
    nav=True,
    label="More pages",
    ),
    brand="Многостраничное приложение Demo",
    color="primary",
    dark="True",
    className="mb-2",
)

app.layout=dbc.Container(
        [navbar, dash.page_container],
        fluid=True,
)

if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=True)