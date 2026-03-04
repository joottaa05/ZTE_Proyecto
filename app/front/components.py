import reflex as rx
from app.back.database import Database
from app.back.auth import AuthState
from typing import Dict, Any

class MobileRowState(rx.State):
    expanded_items: dict[str, bool] = {}

    def toggle(self, id_val: Any):
        # Convertimos a string para usar como llave del dict
        id_str = str(id_val)
        self.expanded_items[id_str] = ~self.expanded_items.get(id_str, False)

def navbar():
    return rx.flex(
        rx.link(rx.text("ZTE Watcher", font_weight="bold", size="5", color="#005C97"), href="/", underline="none"),
        rx.spacer(),
        rx.hstack(
            rx.menu.root(
                rx.menu.trigger(
                    rx.button(
                        rx.flex(rx.icon("layout-dashboard", size=18), rx.text("Recursos", display=["none", "inline"]), rx.icon("chevron-down", size=14), spacing="2", align="center"), 
                        variant="surface", radius="full"
                    )
                ),
                rx.menu.content(
                    rx.menu.item(rx.flex(rx.icon("chart-pie", size=16), "TOTAL", spacing="2"), on_select=lambda: Database.go_to_details("TOTAL GLOBAL")),
                    rx.menu.separator(),
                    rx.foreach(Database.group_names, lambda name: rx.menu.item(name, on_select=lambda: Database.go_to_details(name))),
                ),
            ),
            rx.button(rx.icon("log-out", size=18), color_scheme="red", variant="soft", on_click=AuthState.logout, radius="full"),
            rx.color_mode.button(radius="full"), 
            spacing="3"
        ),
        padding="0.8em 2em", width="100%", 
        bg=rx.color_mode_cond("white", "#111113"), 
        position="fixed", top="0", z_index="100", 
        border_bottom=rx.color_mode_cond("1px solid #E5E7EB", "1px solid #334155")
    )

def pc_view(row: Dict[str, Any]):
    return rx.table.row(
        rx.table.cell(row["IdProceso"], font_weight="bold"),
        rx.table.cell(row["FechaAlta"]),
        rx.table.cell(rx.badge(row["Estado"], variant="soft", color_scheme="blue")),
        rx.table.cell(rx.badge(row["Prioridad"], variant="solid", color_scheme=rx.cond(row["Prioridad"] == "ALTA", "red", rx.cond(row["Prioridad"] == "MEDIA", "orange", "green")))),
        rx.table.cell(row["Descripcion"]),
    )

def mobile_view(row: Dict[str, Any]):
    # El ID se extrae como Var para el estado
    row_id = row["IdProceso"]
    is_expanded = MobileRowState.expanded_items[row_id.to(str)]

    return rx.box(
        rx.vstack(
            rx.flex(
                rx.hstack(
                    rx.text(f"ID: {row['IdProceso']}", font_weight="bold"),
                    rx.icon(rx.cond(is_expanded, "chevron-up", "chevron-down"), size=16),
                    spacing="2", align="center"
                ),
                rx.badge(
                    row["Prioridad"], 
                    variant="solid", 
                    color_scheme=rx.cond(row["Prioridad"] == "ALTA", "red", rx.cond(row["Prioridad"] == "MEDIA", "orange", "green"))
                ),
                justify="between", width="100%",
                on_click=lambda: MobileRowState.toggle(row_id),
                cursor="pointer"
            ),
            rx.cond(
                is_expanded,
                rx.vstack(
                    rx.separator(size="4", margin_y="0.5em"),
                    # CORRECCIÓN AQUÍ: rx.text.span en lugar de rx.span
                    rx.text(rx.text.span("Fecha: ", font_weight="bold"), row["FechaAlta"], size="2"),
                    rx.text(rx.text.span("Estado: ", font_weight="bold"), row["Estado"], size="2"),
                    rx.text(rx.text.span("Descripción: ", font_weight="bold"), row["Descripcion"], size="2"),
                    spacing="1", align_items="start", width="100%"
                )
            ),
            spacing="2", align_items="start"
        ),
        padding="1.2em", 
        border_bottom=rx.color_mode_cond("1px solid #F1F5F9", "1px solid #334155"),
        width="100%"
    )

def get_pie_chart(ds, cat_name):
    return rx.recharts.pie_chart(
        rx.recharts.pie(data=ds, data_key="value", name_key="name", cx="50%", cy="50%", outer_radius="80%", on_click=lambda: Database.go_to_details(cat_name)),
        rx.recharts.graphing_tooltip(), rx.recharts.legend(vertical_align="bottom"), width="100%", height=300,
    )