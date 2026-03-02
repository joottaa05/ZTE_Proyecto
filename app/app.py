import reflex as rx
from app.back.database import Database
from app.front.components import navbar, get_pie_chart, pc_view, mobile_view

def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.vstack(
            rx.heading("PANEL DE CONTROL ZTE", size="9", margin_top="1.5em", margin_bottom="0.25em", color="#005C97", font_weight="extrabold", text_align="center", width="100%", display=["none", "none", "block"]),
            rx.vstack(
                rx.text("TOTAL GLOBAL", font_weight="bold", size="5"),
                get_pie_chart(Database.total_data, "TOTAL GLOBAL"),
                padding="2em", bg=rx.color_mode_cond("white", "#1E1E20"), border_radius="25px", width="100%", border="1px solid #E5E7EB", box_shadow="0px 10px 30px rgba(0,0,0,0.08)", align_items="center",
                margin_top=["5em", "5em", "0.5em"]
            ),
            rx.grid(
                rx.foreach(Database.group_names, lambda name: rx.vstack(
                    rx.text(name, font_weight="bold", size="5"),
                    get_pie_chart(Database.categorized_data[name], name),
                    padding="2em", bg=rx.color_mode_cond("white", "#1E1E20"), border_radius="25px", width="100%", border="1px solid #E5E7EB", box_shadow="0px 10px 30px rgba(0,0,0,0.05)", align_items="center"
                )),
                columns=rx.breakpoints(initial="1", sm="2"), spacing="7", width="100%", margin_top="2em"
            ),
            padding="2em", max_width="1200px", margin="auto", align_items="center", spacing="0"
        ),
        on_mount=Database.load_data
    )

def details() -> rx.Component:
    return rx.box(
        navbar(),
        rx.vstack(
            rx.heading(f"Recurso: {Database.selected_category}", size="8", margin_top="1.5em", margin_bottom="0.5em", color="#005C97", font_weight="bold", text_align="center", width="100%", display=["none", "none", "block"]),
            rx.flex(
                rx.input(placeholder="Buscar...", on_change=Database.set_search_text, flex="1", variant="classic", radius="full"),
                rx.select(["TODAS", "Alta", "Media", "Baja"], on_change=Database.set_priority_filter, width="120px", radius="full"),
                width="100%", spacing="3", margin_top=["5em", "5em", "0em"]
            ),
            rx.box(
                rx.table.root(
                    rx.table.header(rx.table.row(rx.table.column_header_cell("ID"), rx.table.column_header_cell("FECHA ALTA"), rx.table.column_header_cell("ESTADO"), rx.table.column_header_cell("PRIORIDAD"), rx.table.column_header_cell("DESCRIPCIÓN"), bg=rx.color_mode_cond("#F9FAFB", "#111113"))),
                    rx.table.body(rx.foreach(Database.filtered_rows, pc_view)),
                    width="100%", variant="surface", border_radius="15px",
                ),
                display=["none", "none", "block"], width="100%"
            ),
            rx.box(
                rx.vstack(rx.foreach(Database.filtered_rows, mobile_view), spacing="0", width="100%"),
                display=["block", "block", "none"], width="100%", border="1px solid #E5E7EB", border_radius="15px", overflow="hidden"
            ),
            rx.button("← Volver", on_click=rx.redirect("/"), variant="soft", size="3", radius="full"),
            padding="2em", width="100%", max_width="1200px", margin="auto", align_items="center", spacing="5"
        ),
        on_mount=Database.load_data
    )

app = rx.App(theme=rx.theme(accent_color="blue", radius="large"))
app.add_page(index, route="/")
app.add_page(details, route="/details")