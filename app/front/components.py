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
                        rx.flex(rx.icon("layout-dashboard", size=18), "Recursos", rx.icon("chevron-down", size=14), spacing="2", align="center"), 
                        variant="surface", radius="full"
                    )
                ),
                rx.menu.content(
                    rx.menu.item(
                        rx.flex(rx.icon("chart-pie", size=16), "TOTAL", spacing="2", align="center"), 
                        on_select=lambda: Database.go_to_details("TOTAL GLOBAL")
                    ),
                    rx.menu.separator(),
                    rx.foreach(Database.group_names, lambda name: rx.menu.item(name, on_select=lambda: Database.go_to_details(name))),
                ),
            ),
            rx.color_mode.button(radius="full"), spacing="4"
        ),
        padding="0.8em 2em", width="100%", bg=rx.color_mode_cond("white", "#111113"), position="fixed", top="0", z_index="100", border_bottom="1px solid #E5E7EB"
    )

def pc_view(row: rx.Var[dict]):
    return rx.table.row(
        rx.table.cell(row["IdProceso"], font_weight="bold"),
        rx.table.cell(row["FechaAlta"]),
        rx.table.cell(rx.badge(row["Estado"], variant="soft", color_scheme="blue")),
        rx.table.cell(
            rx.badge(
                row["Prioridad"], 
                variant="solid", 
                color_scheme=rx.cond(
                    row["Prioridad"] == "ALTA", "red", 
                    rx.cond(row["Prioridad"] == "MEDIA", "orange", "green")
                )
            )
        ),
        rx.table.cell(row["Descripcion"]),
    )

def mobile_view(row: rx.Var[dict]):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.box(
                rx.flex(
                    rx.vstack(rx.text(f"ID: {row['IdProceso']}", font_weight="bold"), rx.text(row["FechaAlta"], size="1", color="gray"), align_items="start", spacing="0"),
                    rx.badge(row["Prioridad"], variant="solid", color_scheme=rx.cond(row["Prioridad"] == "ALTA", "red", rx.cond(row["Prioridad"] == "MEDIA", "orange", "green"))),
                    justify="between", align="center", width="100%"
                ),
                padding="1.2em", border_bottom="1px solid #EEE", width="100%", cursor="pointer"
            )
        ),
        rx.dialog.content(
            rx.dialog.title(f"Detalle: {row['IdProceso']}"),
            rx.vstack(rx.flex(rx.text("Estado:"), rx.badge(row["Estado"], color_scheme="blue"), justify="between", width="100%"), rx.text(row["Descripcion"], size="2"), spacing="3"),
            rx.flex(rx.dialog.close(rx.button("Cerrar", variant="soft")), margin_top="1.5em", justify="end"),
        )
    )

def get_pie_chart(ds, cat_name):
    return rx.recharts.pie_chart(
        rx.recharts.pie(data=ds, data_key="value", name_key="name", cx="50%", cy="50%", outer_radius="80%", on_click=lambda: Database.go_to_details(cat_name)),
        rx.recharts.graphing_tooltip(), rx.recharts.legend(vertical_align="bottom"), width="100%", height=300,
    )