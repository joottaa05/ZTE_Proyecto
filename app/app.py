import reflex as rx
from app.back.database import Database
from app.back.auth import AuthState
from app.front.components import navbar, get_pie_chart, pc_view, mobile_view
from app.front.login import login_page

FONDO_AZUL = "radial-gradient(circle at center, #1e293b 0%, #0f172a 100%)"

def index() -> rx.Component:
    return rx.fragment(
        rx.cond(
            AuthState.logged_in,
            rx.box(
                navbar(),
                rx.vstack(
                    rx.vstack(
                        rx.text("TOTAL GLOBAL", font_weight="bold", size="5", color="white"),
                        get_pie_chart(Database.total_data, "TOTAL GLOBAL"),
                        padding="2em", bg=rx.color_mode_cond("white", "#1E1E20"), border_radius="25px", width="100%", border="1px solid #334155", margin_top="5em"
                    ),
                    rx.grid(
                        rx.foreach(Database.group_names, lambda name: rx.vstack(
                            rx.text(name, font_weight="bold", size="5", color="white"),
                            get_pie_chart(Database.categorized_data[name], name),
                            padding="2em", bg=rx.color_mode_cond("white", "#1E1E20"), border_radius="25px", width="100%", border="1px solid #334155"
                        )),
                        columns=rx.breakpoints(initial="1", sm="2"), spacing="7", width="100%", margin_top="2em"
                    ),
                    padding="2em", max_width="1200px", margin="auto"
                ),
                background=FONDO_AZUL, min_height="100vh", on_mount=Database.load_data
            ),
            rx.center(on_mount=rx.redirect("/login"))
        )
    )

def details() -> rx.Component:
    return rx.fragment(
        rx.cond(
            AuthState.logged_in,
            rx.box(
                navbar(),
                rx.vstack(
                    rx.heading(f"Recurso: {Database.selected_category}", size="7", color="white", width="100%", text_align="center", margin_top="2.5em"),
                    rx.flex(
                        rx.input(placeholder="Buscar...", on_change=Database.set_search_text, flex="1", radius="full"),
                        rx.select(["TODAS", "ALTA", "MEDIA", "BAJA"], on_change=Database.set_priority_filter, width="120px", radius="full"),
                        width="100%", spacing="3", margin_top=["5em", "5em", "0.5em"] 
                    ),
                    rx.box(
                        rx.table.root(
                            rx.table.header(rx.table.row(rx.table.column_header_cell("ID"), rx.table.column_header_cell("FECHA"), rx.table.column_header_cell("ESTADO"), rx.table.column_header_cell("PRIORIDAD"), rx.table.column_header_cell("DESCRIPCIÓN"))),
                            rx.table.body(rx.foreach(Database.filtered_rows, pc_view)),
                            width="100%", variant="surface", border_radius="15px",
                        ),
                        display=["none", "none", "block"], width="100%"
                    ),
                    rx.box(
                        rx.vstack(rx.foreach(Database.filtered_rows, mobile_view), spacing="0", width="100%"),
                        display=["block", "block", "none"], width="100%", border="1px solid #334155", border_radius="15px", overflow="hidden"
                    ),
                    rx.button("← Volver", on_click=rx.redirect("/"), variant="soft", radius="full"),
                    padding="2em", max_width="1200px", margin="auto", spacing="5"
                ),
                background=FONDO_AZUL, min_height="100vh", on_mount=Database.load_data
            ),
            rx.center(on_mount=rx.redirect("/login"))
        )
    )

app = rx.App(theme=rx.theme(accent_color="blue", radius="large"))
app.add_page(login_page, route="/login")
app.add_page(index, route="/")
app.add_page(details, route="/details")