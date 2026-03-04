import reflex as rx
from app.back.database import Database
from app.back.auth import AuthState
from app.front.components import navbar, get_pie_chart, pc_view, mobile_view
from app.front.login import login_page

# Definición de estilos reutilizables
FONDO_ADAPTABLE = rx.color_mode_cond("#F8FAFC", "#0f172a")
CARD_BG = rx.color_mode_cond("white", "#1E1E20")
CARD_BORDER = rx.color_mode_cond("1px solid #E5E7EB", "1px solid #334155")

def index() -> rx.Component:
    return rx.fragment(
        rx.cond(
            AuthState.logged_in,
            rx.box(
                navbar(),
                rx.vstack(
                    rx.box(
                        rx.heading("ESTADO GLOBAL", size="6", margin_bottom="1em", text_align="center"),
                        get_pie_chart(Database.total_data, "TOTAL GLOBAL"),
                        padding="1.5em", bg=CARD_BG, border_radius="20px", width="100%", border=CARD_BORDER
                    ),
                    rx.grid(
                        rx.foreach(Database.group_names, lambda name: rx.vstack(
                            rx.heading(name, size="4", margin_bottom="0.5em"),
                            get_pie_chart(Database.categorized_data[name], name),
                            padding="1.5em", bg=CARD_BG, border_radius="20px", width="100%", border=CARD_BORDER, align="center"
                        )),
                        columns=rx.breakpoints(initial="1", sm="2"), spacing="5", width="100%"
                    ),
                    padding_top="6em", padding_x=["1em", "2em"], padding_bottom="2em", max_width="1200px", margin="auto", spacing="6"
                ),
                background=FONDO_ADAPTABLE, min_height="100vh", on_mount=Database.load_data
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
                    rx.heading(f"Recurso: {Database.selected_category}", size="6", text_align="center", width="100%"),
                    rx.flex(
                        rx.input(placeholder="Buscar...", on_change=Database.set_search_text, flex="1", radius="full"),
                        rx.select(["TODAS", "ALTA", "MEDIA", "BAJA"], on_change=Database.set_priority_filter, width="110px", radius="full"),
                        width="100%", spacing="2"
                    ),
                    # Tabla PC
                    rx.box(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("ID"), 
                                    rx.table.column_header_cell("FECHA"), 
                                    rx.table.column_header_cell("ESTADO"), 
                                    rx.table.column_header_cell("PRIORIDAD"), 
                                    rx.table.column_header_cell("DESCRIPCIÓN")
                                )
                            ),
                            rx.table.body(rx.foreach(Database.filtered_rows, pc_view)),
                            width="100%", variant="surface"
                        ),
                        display=["none", "none", "block"], width="100%"
                    ),
                    # Lista Móvil
                    rx.box(
                        rx.vstack(rx.foreach(Database.filtered_rows, mobile_view), spacing="0", width="100%"),
                        display=["block", "block", "none"], 
                        width="100%", bg=CARD_BG, border_radius="15px", overflow="hidden", border=CARD_BORDER
                    ),
                    rx.button("← VOLVER", on_click=rx.redirect("/"), variant="soft", width="100%", size="3"),
                    padding_top="6em", padding_x=["1em", "2em"], max_width="1200px", margin="auto", spacing="5", padding_bottom="2em"
                ),
                background=FONDO_ADAPTABLE, min_height="100vh", on_mount=Database.load_data
            ),
            rx.center(on_mount=rx.redirect("/login"))
        )
    )

app = rx.App(
    theme=rx.theme(
        accent_color="blue", 
        radius="large", 
        appearance="light" 
    )
)
app.add_page(login_page, route="/login")
app.add_page(index, route="/")
app.add_page(details, route="/details")