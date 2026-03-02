import reflex as rx
from app.back.database import Database

def navbar():
    return rx.flex(
        rx.link(rx.text("ZTE Watcher", font_weight="bold", size="5", color="#005C97"), href="/", underline="none"),
        rx.spacer(),
        rx.hstack(
            rx.menu.root(
                rx.menu.trigger(
                    rx.button(
                        rx.flex(rx.icon("layout-dashboard", size=18), rx.text("Recursos"), rx.icon("chevron-down", size=14), spacing="2", align="center"),
                        variant="surface", color_scheme="gray", radius="full", cursor="pointer",
                    ),
                ),
                rx.menu.content(
                    rx.menu.item(rx.flex(rx.icon("pie-chart", size=16), "TOTAL", spacing="2"), on_select=lambda: Database.go_to_details("TOTAL GLOBAL")),
                    rx.menu.separator(),
                    rx.foreach(Database.group_names, lambda name: rx.menu.item(name, on_select=lambda: Database.go_to_details(name))),
                    width="180px", variant="soft", high_contrast=True,
                ),
            ),
            rx.color_mode.button(radius="full"),
            spacing="4", align="center",
        ),
        padding="0.8em 2em", width="100%", bg=rx.color_mode_cond("white", "#111113"),
        position="fixed", top="0", z_index="100", border_bottom="1px solid #E5E7EB", align="center"
    )

def pc_view(row: dict):
    return rx.table.row(
        rx.table.cell(row["IdProceso"], font_weight="bold", color="#005C97"),
        rx.table.cell(row["FechaAlta"]),
        rx.table.cell(rx.badge(row["Estado"], variant="surface", color_scheme="blue")),
        rx.table.cell(rx.badge(row["Prioridad"], variant="solid", color_scheme=rx.cond(row["Prioridad"] == "Alta", "red", rx.cond(row["Prioridad"] == "Media", "orange", "green")))),
        rx.table.cell(row["Descripcion"], font_style="italic"),
    )

def mobile_view(row: dict):
    """Vista móvil: Muestra ID y Prioridad. El Estado va al Pop-up."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.box(
                rx.flex(
                    rx.vstack(
                        rx.text(f"ID: {row['IdProceso']}", font_weight="bold", size="3"),
                        rx.text(row["FechaAlta"], size="1", color="gray"),
                        align_items="start", spacing="0"
                    ),
                    # PRIORIDAD EN LA VISTA PRINCIPAL
                    rx.badge(
                        row["Prioridad"], 
                        variant="solid", 
                        size="2",
                        color_scheme=rx.cond(row["Prioridad"] == "Alta", "red", rx.cond(row["Prioridad"] == "Media", "orange", "green"))
                    ),
                    justify="between", align="center", width="100%"
                ),
                padding="1.2em", border_bottom="1px solid #EEE", cursor="pointer", width="100%",
                _hover={"bg": rx.color_mode_cond("#F9FAFB", "#1A1A1B")}
            )
        ),
        rx.dialog.content(
            rx.dialog.title(f"Detalle: {row['IdProceso']}"),
            rx.vstack(
                rx.divider(),
                rx.flex(rx.text("Estado:", font_weight="bold"), rx.badge(row["Estado"], variant="surface"), justify="between", width="100%"),
                rx.flex(rx.text("Prioridad:", font_weight="bold"), 
                        rx.badge(row["Prioridad"], variant="solid", color_scheme=rx.cond(row["Prioridad"] == "Alta", "red", "green")), 
                        justify="between", width="100%"),
                rx.vstack(
                    rx.text("Descripción:", font_weight="bold"),
                    rx.text(row["Descripcion"], size="2", color=rx.color_mode_cond("#4B5563", "#D1D5DB")),
                    align_items="start", width="100%", bg=rx.color_mode_cond("#F3F4F6", "#2D2D2E"), padding="1em", border_radius="8px"
                ),
                spacing="3", margin_top="1em"
            ),
            rx.flex(rx.dialog.close(rx.button("Cerrar", variant="soft", color_scheme="gray")), margin_top="1.5em", justify="end"),
            max_width="400px", border_radius="20px"
        )
    )

def get_pie_chart(ds, cat_name):
    return rx.recharts.pie_chart(
        rx.recharts.pie(data=ds, data_key="value", name_key="name", cx="50%", cy="50%", outer_radius="80%", stroke="none", on_click=lambda: Database.go_to_details(cat_name)),
        rx.recharts.graphing_tooltip(), width="100%", height=300,
    )