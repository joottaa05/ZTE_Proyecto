import reflex as rx
from app.back.database import Database

def navbar():
    return rx.flex(
        rx.link(rx.text("ZTE Watcher", font_weight="bold", size="5", color="#005C97"), href="/", underline="none"),
        rx.spacer(),
        rx.color_mode.button(),
        padding="1em 2em", width="100%", bg=rx.color_mode_cond("white", "#111113"),
        position="fixed", top="0", z_index="100", border_bottom="1px solid #E5E7EB", align="center"
    )

def get_pie_chart(ds, cat_name):
    return rx.recharts.pie_chart(
        rx.recharts.pie(
            data=ds, data_key="value", name_key="name",
            cx="50%", cy="50%", outer_radius="80%", stroke="none",
            on_click=lambda: Database.go_to_details(cat_name),
        ),
        rx.recharts.graphing_tooltip(),
        width="100%", height=300,
    )

def pc_view(row: dict):
    return rx.table.row(
        rx.table.cell(row["IdProceso"], font_weight="bold", color="#005C97"),
        rx.table.cell(row["FechaAlta"]),
        rx.table.cell(rx.badge(row["Estado"], variant="surface", color_scheme="blue")),
        rx.table.cell(
            rx.badge(
                row["Prioridad"], 
                variant="solid",
                color_scheme=rx.cond(row["Prioridad"] == "Alta", "red", rx.cond(row["Prioridad"] == "Media", "orange", "green"))
            )
        ),
        rx.table.cell(row["Descripcion"], font_style="italic", color=rx.color_mode_cond("#444", "#ccc")),
        _hover={"bg": rx.color_mode_cond("#F9FAFB", "#1A1A1B")},
        display=["none", "none", "table-row"]
    )

def mobile_view(row: dict):
    return rx.box(
        rx.dialog.root(
            rx.dialog.trigger(
                rx.flex(
                    rx.vstack(
                        rx.text(f"ID: {row['IdProceso']}", font_weight="bold", color="#005C97"),
                        rx.badge(row["Prioridad"], color_scheme=rx.cond(row["Prioridad"] == "Alta", "red", "green")),
                        align_items="start",
                    ),
                    rx.icon("chevron-right", color="gray"),
                    justify="between", align="center", padding="1em", border_bottom="1px solid #EEE"
                )
            ),
            rx.dialog.content(
                rx.dialog.title(f"Detalle Proceso {row['IdProceso']}"),
                rx.vstack(
                    rx.text(f"Estado: {row['Estado']}"), 
                    rx.text(f"Fecha: {row['FechaAlta']}"), 
                    rx.text(f"Descripción: {row['Descripcion']}", color="gray"),
                    spacing="2"
                ),
                rx.dialog.close(rx.button("Cerrar", margin_top="1em", variant="soft"))
            )
        ),
        display=["block", "block", "none"]
    )