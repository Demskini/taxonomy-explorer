"""
Dash frontend for the taxonomy explorer project.

This file defines the user interface for the taxonomy explorer.
It provides a search page where users can enter a keyword, choose
a search mode, view matching taxonomy records, and click into
a taxon details page.
"""

from urllib.parse import urlencode, parse_qs, quote, unquote

import requests
from dash import Dash, html, dcc, Input, Output, State, dash_table, callback_context
from dash.exceptions import PreventUpdate

API_BASE_URL = "http://127.0.0.1:8000"

# Northeastern inspired colors
PRIMARY_RED = "#C8102E"
DARK = "#2D2A26"
LIGHT_BG = "#F7F7F8"
CARD_BG = "#FFFFFF"
BORDER = "#D9D9DD"
TEXT = "#1F1F1F"
MUTED = "#666666"

app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Taxonomy Explorer"


def build_search_query(keyword: str, mode: str, page: int = 1, per_page: int = 10) -> str:
    """Build a query string that preserves the current search settings."""
    return "?" + urlencode(
        {
            "keyword": keyword,
            "mode": mode,
            "page": page,
            "per_page": per_page,
        }
    )


def page_wrapper(children):
    """Shared page wrapper for a cleaner centered layout."""
    return html.Div(
        children,
        style={
            "maxWidth": "1000px",
            "margin": "40px auto",
            "padding": "30px",
            "backgroundColor": CARD_BG,
            "border": f"1px solid {BORDER}",
            "borderRadius": "14px",
            "boxShadow": "0 6px 18px rgba(0, 0, 0, 0.06)",
            "fontFamily": "Arial, sans-serif",
            "color": TEXT,
        },
    )


def section_heading(text):
    return html.H3(
        text,
        style={
            "color": PRIMARY_RED,
            "marginTop": "28px",
            "marginBottom": "12px",
            "borderBottom": f"2px solid {BORDER}",
            "paddingBottom": "6px",
        },
    )


def styled_table(headers, rows):
    """Reusable HTML table styling."""
    return html.Table(
        [
            html.Thead(
                html.Tr(
                    [html.Th(h, style={"padding": "12px", "textAlign": "center"}) for h in headers],
                    style={"backgroundColor": LIGHT_BG, "color": DARK},
                )
            ),
            html.Tbody(rows),
        ],
        style={
            "width": "100%",
            "borderCollapse": "collapse",
            "marginTop": "12px",
            "border": f"1px solid {BORDER}",
            "borderRadius": "8px",
            "overflow": "hidden",
        },
    )


def search_layout():
    """Build the main search page layout."""
    return page_wrapper(
        [
            html.H1(
                "Taxonomy Explorer",
                style={"color": PRIMARY_RED, "marginBottom": "8px", "fontSize": "42px"},
            ),
            html.P(
                "Search taxonomy names and explore related taxa.",
                style={"color": MUTED, "marginBottom": "24px", "fontSize": "18px"},
            ),
            html.Div(
                [
                    dcc.Input(
                        id="keyword-input",
                        type="text",
                        placeholder="Enter a keyword",
                        style={
                            "width": "300px",
                            "marginRight": "10px",
                            "padding": "10px",
                            "borderRadius": "8px",
                            "border": f"1px solid {BORDER}",
                        },
                    ),
                    dcc.Dropdown(
                        id="mode-dropdown",
                        options=[
                            {"label": "Contains", "value": "contains"},
                            {"label": "Starts With", "value": "starts_with"},
                            {"label": "Ends With", "value": "ends_with"},
                        ],
                        value="contains",
                        clearable=False,
                        style={
                            "width": "220px",
                            "display": "inline-block",
                            "marginRight": "10px",
                        },
                    ),
                    dcc.Dropdown(
                        id="per-page-dropdown",
                        options=[
                            {"label": "10 per page", "value": 10},
                            {"label": "25 per page", "value": 25},
                            {"label": "50 per page", "value": 50},
                            {"label": "100 per page", "value": 100},
                        ],
                        value=10,
                        clearable=False,
                        style={
                            "width": "150px",
                            "display": "inline-block",
                            "marginRight": "10px",
                        },
                    ),
                    html.Button(
                        "Search",
                        id="search-button",
                        n_clicks=0,
                        style={
                            "backgroundColor": PRIMARY_RED,
                            "color": "white",
                            "border": "none",
                            "padding": "11px 18px",
                            "borderRadius": "8px",
                            "cursor": "pointer",
                            "fontWeight": "bold",
                        },
                    ),
                ],
                style={"marginBottom": "20px"},
            ),
            html.Div(
                id="results-summary",
                style={"marginBottom": "10px", "fontWeight": "bold", "color": DARK},
            ),
            dash_table.DataTable(
                id="results-table",
                columns=[
                    {"name": "Taxon ID", "id": "tax_id", "presentation": "markdown"},
                    {"name": "Name", "id": "name_txt"},
                    {"name": "Name Class", "id": "name_class"},
                ],
                data=[],
                style_table={"overflowX": "auto", "border": f"1px solid {BORDER}", "borderRadius": "8px"},
                style_cell={
                    "textAlign": "center",
                    "padding": "12px",
                    "fontSize": "16px",
                    "border": f"1px solid {BORDER}",
                },
                style_header={
                    "fontWeight": "bold",
                    "backgroundColor": LIGHT_BG,
                    "color": DARK,
                    "textAlign": "center",
                },
                markdown_options={"link_target": "_self"},
            ),
            html.Br(),
            html.Div(
                [
                    html.Button(
                        "Previous",
                        id="prev-button",
                        n_clicks=0,
                        style={
                            "padding": "10px 16px",
                            "borderRadius": "8px",
                            "border": f"1px solid {BORDER}",
                            "backgroundColor": "#FFFFFF",
                            "cursor": "pointer",
                        },
                    ),
                    html.Span(
                        id="page-indicator",
                        style={"margin": "0 15px", "fontWeight": "bold", "color": DARK},
                    ),
                    html.Button(
                        "Next",
                        id="next-button",
                        n_clicks=0,
                        style={
                            "padding": "10px 16px",
                            "borderRadius": "8px",
                            "border": f"1px solid {BORDER}",
                            "backgroundColor": "#FFFFFF",
                            "cursor": "pointer",
                        },
                    ),
                ],
                style={"marginTop": "15px"},
            ),
        ]
    )


def detail_layout():
    """Build the taxon detail page layout."""
    return page_wrapper([html.Div(id="taxon-detail-content")])


app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
    ],
    style={"backgroundColor": LIGHT_BG, "minHeight": "100vh", "padding": "20px"},
)

app.validation_layout = html.Div(
    [
        app.layout,
        search_layout(),
        detail_layout(),
    ]
)


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_page(pathname):
    """Show either the search page or a taxon detail page."""
    if pathname is None or pathname == "/":
        return search_layout()

    if pathname.startswith("/taxon/"):
        return detail_layout()

    return page_wrapper(
        [
            html.H2("Page not found", style={"color": PRIMARY_RED}),
            dcc.Link("Back to Search", href="/", style={"color": PRIMARY_RED}),
        ]
    )


@app.callback(
    Output("keyword-input", "value"),
    Output("mode-dropdown", "value"),
    Output("per-page-dropdown", "value"),
    Input("url", "search"),
)
def populate_search_inputs(search):
    """Fill the search input and dropdown from the URL query string."""
    params = parse_qs(search.lstrip("?")) if search else {}

    keyword = params.get("keyword", [""])[0]
    mode = params.get("mode", ["contains"])[0]
    per_page = int(params.get("per_page", [10])[0])

    if mode not in {"contains", "starts_with", "ends_with"}:
        mode = "contains"

    if per_page not in {10, 25, 50, 100}:
        per_page = 10

    return keyword, mode, per_page


@app.callback(
    Output("url", "search", allow_duplicate=True),
    Input("search-button", "n_clicks"),
    State("keyword-input", "value"),
    State("mode-dropdown", "value"),
    State("per-page-dropdown", "value"),
    prevent_initial_call=True,
)
def update_url_from_search(n_clicks, keyword, mode, per_page):
    """Update the query string when the user clicks Search."""
    if not keyword:
        raise PreventUpdate

    return build_search_query(keyword, mode, page=1, per_page=per_page)


@app.callback(
    Output("url", "search", allow_duplicate=True),
    Input("prev-button", "n_clicks"),
    Input("next-button", "n_clicks"),
    State("url", "search"),
    prevent_initial_call=True,
)
def change_page(prev_clicks, next_clicks, search):
    """Move between pages while preserving the current search settings."""
    params = parse_qs(search.lstrip("?")) if search else {}

    keyword = params.get("keyword", [""])[0]
    mode = params.get("mode", ["contains"])[0]
    page = int(params.get("page", [1])[0])
    per_page = int(params.get("per_page", [10])[0])

    if not keyword:
        raise PreventUpdate

    if not callback_context.triggered:
        raise PreventUpdate

    triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "prev-button" and page > 1:
        page -= 1
    elif triggered_id == "next-button":
        page += 1
    else:
        raise PreventUpdate

    return build_search_query(keyword, mode, page=page, per_page=per_page)


@app.callback(
    Output("results-summary", "children"),
    Output("results-table", "data"),
    Output("page-indicator", "children"),
    Input("url", "search"),
)
def run_search_from_url(search):
    """
    Read the search settings from the URL, call the FastAPI backend,
    and show the current page of results.
    """
    params = parse_qs(search.lstrip("?")) if search else {}

    keyword = params.get("keyword", [""])[0]
    mode = params.get("mode", ["contains"])[0]
    page = int(params.get("page", [1])[0])
    per_page = int(params.get("per_page", [10])[0])

    if not keyword:
        return "Enter a keyword and click Search.", [], "Page 1"

    try:
        response = requests.get(
            f"{API_BASE_URL}/search",
            params={
                "keyword": keyword,
                "mode": mode,
                "page": page,
                "per_page": per_page,
            },
            timeout=5,
        )
    except requests.exceptions.RequestException:
        return "Could not connect to the API. Make sure FastAPI is running on port 8000.", [], f"Page {page}"

    if response.status_code != 200:
        return "Search failed. Please check the API.", [], f"Page {page}"

    data = response.json()

    formatted_results = []
    current_search_query = build_search_query(keyword, mode, page, per_page)
    encoded_back = quote(current_search_query, safe="")

    for result in data["results"]:
        formatted_results.append(
            {
                "tax_id": f"[{result['tax_id']}](/taxon/{result['tax_id']}?back={encoded_back})",
                "name_txt": result["name_txt"],
                "name_class": result["name_class"],
            }
        )

    start_num = (page - 1) * per_page + 1 if data["total_results"] > 0 else 0
    end_num = min(page * per_page, data["total_results"])

    summary = (
        f"Showing results {start_num}-{end_num} "
        f"out of {data['total_results']} total match(es)."
    )

    return summary, formatted_results, f"Page {page}"


@app.callback(
    Output("taxon-detail-content", "children"),
    Input("url", "pathname"),
    Input("url", "search"),
)
def load_taxon_detail(pathname, search):
    """Load and display details for a selected taxon."""
    if not pathname or not pathname.startswith("/taxon/"):
        raise PreventUpdate

    try:
        tax_id = int(pathname.split("/")[-1])
    except ValueError:
        return html.H2("Invalid taxon ID")

    params = parse_qs(search.lstrip("?")) if search else {}

    raw_back = params.get("back", [""])[0]
    decoded_back = unquote(raw_back)

    if decoded_back.startswith("?"):
        back_href = f"/{decoded_back}"
    elif decoded_back.startswith("/"):
        back_href = decoded_back
    else:
        back_href = "/"

    try:
        response = requests.get(
            f"{API_BASE_URL}/taxa",
            params={"tax_id": tax_id},
            timeout=5,
        )
    except requests.exceptions.RequestException:
        return html.Div("Could not connect to the API. Make sure FastAPI is running.")

    if response.status_code == 404:
        return html.Div("Taxon not found.")

    if response.status_code != 200:
        return html.Div("Failed to load taxon details.")

    data = response.json()

    info_cards = html.Div(
        [
            html.Div(
                [html.Div("Taxon ID", style={"color": MUTED, "fontSize": "14px"}), html.Div(str(data["tax_id"]), style={"fontWeight": "bold", "fontSize": "20px"})],
                style={"flex": "1", "padding": "16px", "backgroundColor": LIGHT_BG, "borderRadius": "10px", "border": f"1px solid {BORDER}"},
            ),
            html.Div(
                [html.Div("Rank", style={"color": MUTED, "fontSize": "14px"}), html.Div(data["rank"], style={"fontWeight": "bold", "fontSize": "20px"})],
                style={"flex": "1", "padding": "16px", "backgroundColor": LIGHT_BG, "borderRadius": "10px", "border": f"1px solid {BORDER}"},
            ),
        ],
        style={"display": "flex", "gap": "16px", "marginBottom": "20px"},
    )

    parent_section = html.Div(
        [
            html.Span("Parent: ", style={"fontWeight": "bold", "color": DARK}),
            html.Span("None", style={"color": MUTED}),
        ],
        style={"marginBottom": "20px", "fontSize": "18px"},
    )

    if data["parent"]:
        parent_href = f"/taxon/{data['parent']['tax_id']}?back={quote(back_href, safe='')}"
        parent_section = html.Div(
            [
                html.Span("Parent: ", style={"fontWeight": "bold", "color": DARK}),
                dcc.Link(
                    f"{data['parent']['scientific_name']} ({data['parent']['tax_id']})",
                    href=parent_href,
                    style={"color": PRIMARY_RED, "textDecoration": "none", "fontWeight": "bold"},
                ),
            ],
            style={"marginBottom": "20px", "fontSize": "18px"},
        )

    if data["children"]:
        child_rows = []
        for i, child in enumerate(data["children"]):
            child_href = f"/taxon/{child['tax_id']}?back={quote(back_href, safe='')}"
            child_rows.append(
                html.Tr(
                    [
                        html.Td(
                            dcc.Link(
                                str(child["tax_id"]),
                                href=child_href,
                                style={"color": PRIMARY_RED, "textDecoration": "none", "fontWeight": "bold"},
                            ),
                            style={"padding": "12px", "textAlign": "center"},
                        ),
                        html.Td(child["scientific_name"], style={"padding": "12px", "textAlign": "center"}),
                        html.Td(child["rank"], style={"padding": "12px", "textAlign": "center"}),
                    ],
                    style={"backgroundColor": "#FFFFFF" if i % 2 == 0 else LIGHT_BG},
                )
            )

        children_table = styled_table(
            ["Taxon ID", "Scientific Name", "Rank"],
            child_rows,
        )
    else:
        children_table = html.Div(
            "No children found.",
            style={"padding": "14px", "backgroundColor": LIGHT_BG, "border": f"1px solid {BORDER}", "borderRadius": "8px"},
        )

    name_rows = []
    for i, name in enumerate(data["names"]):
        name_rows.append(
            html.Tr(
                [
                    html.Td(name["name_txt"], style={"padding": "12px", "textAlign": "center"}),
                    html.Td(name["name_class"], style={"padding": "12px", "textAlign": "center"}),
                    html.Td(name["unique_name"] if name["unique_name"] else "—", style={"padding": "12px", "textAlign": "center"}),
                ],
                style={"backgroundColor": "#FFFFFF" if i % 2 == 0 else LIGHT_BG},
            )
        )

    names_table = styled_table(
        ["Name", "Name Class", "Unique Name"],
        name_rows,
    )

    return html.Div(
        [
            html.H1(
                data["scientific_name"] if data["scientific_name"] else f"Taxon {data['tax_id']}",
                style={"color": PRIMARY_RED, "fontSize": "42px", "marginBottom": "8px"},
            ),
            html.P(
                "Taxon detail view",
                style={"color": MUTED, "fontSize": "18px", "marginBottom": "24px"},
            ),
            info_cards,
            parent_section,
            section_heading("Children"),
            children_table,
            section_heading("Names"),
            names_table,
            html.Br(),
            dcc.Link(
                "Back to Search Results",
                href=back_href,
                style={"color": PRIMARY_RED, "fontWeight": "bold", "textDecoration": "none", "fontSize": "18px"},
            ),
        ]
    )


if __name__ == "__main__":
    app.run(debug=True, port=8050)