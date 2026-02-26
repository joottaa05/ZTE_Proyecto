import reflex as rx
from app.back.database import Database
from app.front.components import navbar, get_pie_chart, mobile_view, pc_view

def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.vstack(
            rx.heading("Panel de Control ZTE", size="8", margin_top="3em", margin_bottom="1em"),
            
            # TOTAL GLOBAL unificado con el estilo de las otras tarjetas
            rx.vstack(
                rx.text("TOTAL GLOBAL", font_weight="bold", size="5"),
                get_pie_chart(Database.total_data, "TOTAL GLOBAL"),
                padding="2em", 
                bg=rx.color_mode_cond("white", "#1E1E20"),
                border_radius="20px", 
                width="100%", 
                border="1px solid #E5E7EB",
                margin_bottom="2em"
            ),

            # GRUPO DE RUEDAS POR RECURSO
            rx.grid(
                rx.foreach(Database.group_names, lambda name: rx.vstack(
                    rx.text(name, font_weight="bold", size="5"),
                    get_pie_chart(Database.categorized_data[name], name),
                    padding="2em", bg=rx.color_mode_cond("white", "#1E1E20"),
                    border_radius="20px", width="100%", border="1px solid #E5E7EB"
                )),
                columns=rx.breakpoints(initial="1", sm="2"), 
                spacing="6", width="100%",
            ),
            padding="2em", max_width="1200px", margin="auto"
        ),
        on_mount=Database.load_data
    )

def details() -> rx.Component:
    return rx.box(
        navbar(),
        rx.vstack(
            rx.heading(f"Recurso: {Database.selected_category}", size="7", margin_top="3em"),
            rx.hstack(
                rx.input(placeholder="Buscar...", on_change=Database.set_search_text, flex="1"),
                rx.select(["TODAS", "Alta", "Media", "Baja"], on_change=Database.set_priority_filter, width="150px")
            ),
            rx.box(
                rx.foreach(Database.filtered_rows, mobile_view),
                width="100%", display=["block", "block", "none"],
                border="1px solid #E5E7EB", border_radius="10px", overflow="hidden"
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID"),
                        rx.table.column_header_cell("Fecha"),
                        rx.table.column_header_cell("Estado"),
                        rx.table.column_header_cell("Prioridad"),
                        rx.table.column_header_cell("Descripción"),
                    )
                ),
                rx.table.body(rx.foreach(Database.filtered_rows, pc_view)),
                width="100%", variant="surface", display=["none", "none", "table"]
            ),
            rx.button("← Volver", on_click=rx.redirect("/"), variant="outline"),
            padding="2em", width="100%", max_width="1200px", margin="auto", spacing="5"
        )
    )

app = rx.App(theme=rx.theme(accent_color="blue"))
app.add_page(index, route="/")
app.add_page(details, route="/details")