import reflex as rx
from app.back.database import Database

def navbar():
    return rx.flex(
        rx.link(rx.text("ZTE Watcher", font_weight="bold", size="5"), href="/", underline="none"),
        rx.spacer(),
        rx.color_mode.button(),
        padding="1em 2em", width="100%", bg=rx.color_mode_cond("white", "#111113"),
        position="fixed", top="0", z_index="100", border_bottom="1px solid #E5E7EB"
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

def mobile_view(row: dict):
    return rx.box(
        rx.dialog.root(
            rx.dialog.trigger(
                rx.flex(
                    rx.vstack(
                        rx.text(f"ID: {row['IdProceso']}", font_weight="bold"),
                        rx.badge(row["Prioridad"], color_scheme=rx.cond(row["Prioridad"] == "Alta", "red", "green")),
                        align_items="start",
                    ),
                    rx.icon("chevron-right"),
                    justify="between", align="center", padding="1em", border_bottom="1px solid #EEE"
                )
            ),
            rx.dialog.content(
                rx.dialog.title(f"Detalle {row['IdProceso']}"),
                rx.vstack(rx.text(f"Estado: {row['Estado']}"), rx.text(f"Fecha: {row['FechaAlta']}"), rx.text(f"Descripción: {row['Descripcion']}")),
                rx.dialog.close(rx.button("Cerrar", margin_top="1em"))
            )
        ),
        display=["block", "block", "none"]
    )

def pc_view(row: dict):
    return rx.table.row(
        rx.table.cell(row["IdProceso"]),
        rx.table.cell(row["FechaAlta"]),
        rx.table.cell(row["Estado"]),
        rx.table.cell(row["Prioridad"]),
        rx.table.cell(row["Descripcion"]),
        display=["none", "none", "table-row"]
    )