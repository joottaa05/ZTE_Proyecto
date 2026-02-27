import reflex as rx
from app.back.database import Database
from app.front.components import navbar, get_pie_chart, mobile_view, pc_view

def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.vstack(
            # Título: margen superior reducido a 1.25em (la mitad de antes)
            rx.heading(
                "PANEL DE CONTROL ZTE", 
                size="9", 
                margin_top="1.25em", 
                margin_bottom="0.50em", 
                color="#005C97", 
                font_weight="extrabold",
                text_align="center", 
                width="100%"
            ),
            
            # TOTAL GLOBAL
            rx.vstack(
                rx.text("TOTAL GLOBAL", font_weight="bold", size="5"),
                get_pie_chart(Database.total_data, "TOTAL GLOBAL"),
                padding="2em", 
                bg=rx.color_mode_cond("white", "#1E1E20"),
                border_radius="20px", width="100%", border="1px solid #E5E7EB",
                box_shadow="0px 10px 25px rgba(0,0,0,0.08)",
                margin_bottom="1em"
            ),

            # GRUPO DE RECURSOS
            rx.grid(
                rx.foreach(Database.group_names, lambda name: rx.vstack(
                    rx.text(name, font_weight="bold", size="5"),
                    get_pie_chart(Database.categorized_data[name], name),
                    padding="2em", bg=rx.color_mode_cond("white", "#1E1E20"),
                    border_radius="20px", width="100%", border="1px solid #E5E7EB",
                    box_shadow="0px 10px 25px rgba(0,0,0,0.05)",
                )),
                columns=rx.breakpoints(initial="1", sm="2"), 
                spacing="6", width="100%",
            ),
            padding="2em", max_width="1200px", margin="auto",
            spacing="0"
        ),
        on_mount=Database.load_data
    )

def details() -> rx.Component:
    return rx.box(
        navbar(),
        rx.vstack(
            # Título de detalles: margen también reducido a 1.25em
            rx.heading(
                f"Recurso: {Database.selected_category}", 
                size="8", 
                margin_top="1.25em", 
                margin_bottom="0.5em", 
                color="#005C97", 
                font_weight="bold"
            ),
            rx.flex(
                rx.input(placeholder="Buscar por ID o texto...", on_change=Database.set_search_text, flex="1", variant="classic"),
                rx.select(["TODAS", "Alta", "Media", "Baja"], on_change=Database.set_priority_filter, width="150px"),
                width="100%", spacing="3"
            ),
            # TABLA PREMIUM
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID"),
                        rx.table.column_header_cell("FECHA ALTA"),
                        rx.table.column_header_cell("ESTADO"),
                        rx.table.column_header_cell("PRIORIDAD"),
                        rx.table.column_header_cell("DESCRIPCIÓN"),
                        bg=rx.color_mode_cond("#F3F4F6", "#111113")
                    )
                ),
                rx.table.body(rx.foreach(Database.filtered_rows, pc_view)),
                width="100%", variant="surface", border_radius="15px", overflow="hidden",
                box_shadow="0px 4px 15px rgba(0,0,0,0.05)",
                display=["none", "none", "table"]
            ),
            rx.box(
                rx.foreach(Database.filtered_rows, mobile_view),
                width="100%", display=["block", "block", "none"],
                border="1px solid #E5E7EB", border_radius="15px", overflow="hidden"
            ),
            rx.button("← Volver al Panel", on_click=rx.redirect("/"), variant="outline", size="3"),
            padding="2em", width="100%", max_width="1200px", margin="auto", spacing="4"
        )
    )

app = rx.App(theme=rx.theme(accent_color="blue", radius="large"))
app.add_page(index, route="/")
app.add_page(details, route="/details")