from typing import Any, Dict

import reflex as rx
from app.back.auth import AuthState
from app.back.database import ESTADOS_VALIDOS, Database, get_color_scheme


class MobileRowState(rx.State):
    expanded_items: dict[str, bool] = {}

    def toggle(self, id_val: str):
        id_str = str(id_val)
        current = self.expanded_items.get(id_str, False)
        self.expanded_items[id_str] = not current


def navbar():
    return rx.flex(
        rx.link(
            rx.text("ZTE Watcher", font_weight="bold", size="5", color="#005C97"),
            href="/",
            underline="none",
        ),
        rx.spacer(),
        rx.hstack(
            rx.menu.root(
                rx.menu.trigger(
                    rx.button(
                        rx.flex(
                            rx.icon("layout-dashboard", size=18),
                            rx.text("Grupos", display=["none", "inline"]),
                            rx.icon("chevron-down", size=14),
                            spacing="2",
                            align="center",
                        ),
                        variant="surface",
                        radius="full",
                    )
                ),
                rx.menu.content(
                    rx.menu.item(
                        rx.flex(rx.icon("chart-pie", size=16), "TOTAL", spacing="2"),
                        on_select=lambda: Database.go_to_details("TOTAL GLOBAL"),
                    ),
                    rx.menu.separator(),
                    rx.foreach(
                        Database.group_names,
                        lambda name: rx.menu.item(
                            name, on_select=lambda: Database.go_to_details(name)
                        ),
                    ),
                ),
            ),
            rx.button(
                rx.icon("log-out", size=18),
                color_scheme="red",
                variant="soft",
                on_click=AuthState.logout,
                radius="full",
            ),
            rx.color_mode.button(radius="full"),
            spacing="3",
        ),
        padding="0.8em 2em",
        width="100%",
        bg=rx.color_mode_cond("white", "#111113"),
        position="fixed",
        top="0",
        z_index="100",
        border_bottom=rx.color_mode_cond("1px solid #E5E7EB", "1px solid #334155"),
    )


def _badge_color(color_val: str) -> rx.Component:
    return rx.badge(
        color_val,
        variant="solid",
        color_scheme=rx.cond(
            color_val == "ROJO",
            "red",
            rx.cond(color_val == "NARANJA", "orange", "green"),
        ),
    )


def _estado_chip(row: Dict[str, Any]) -> rx.Component:
    # Texto del chip: si hay estado_resolucion, lo usamos; si no, "SIN ESTADO"
    estado_texto = rx.cond(
        row["estado_resolucion"] == "",
        "SIN ESTADO",
        row["estado_resolucion"],
    )
    return rx.badge(
        rx.text(
            estado_texto,
            size="2",
            font_weight="500",
        ),
        variant="solid",
        color_scheme=rx.cond(
            row["color"] == "ROJO",
            "red",
            rx.cond(row["color"] == "NARANJA", "orange", "green"),
        ),
        padding_x="0.8em",
        padding_y="0.4em",
        radius="large",
    )


def pc_view(row: Dict[str, Any]) -> rx.Component:
    return rx.table.row(
        rx.table.cell(row["fecha"]),  # FECHA primero
        rx.table.cell(row["id"], font_weight="bold"),
        rx.table.cell(row["web"]),
        rx.cond(
            Database.selected_category == "TOTAL GLOBAL",
            rx.table.cell(row["grupo"]),
        ),
        rx.table.cell(_estado_chip(row)),  # estado en chip coloreado
        rx.table.cell(row["descripcion"]),  # Descripción al final
    )


def mobile_view(row: Dict[str, Any]) -> rx.Component:
    row_id = str(row["id"])
    is_expanded = MobileRowState.expanded_items.get(row_id, False)
    return rx.box(
        rx.vstack(
            rx.flex(
                rx.hstack(
                    rx.text(f"{row['fecha']} · ID: {row['id']}", font_weight="bold"),
                    rx.icon(rx.cond(is_expanded, "chevron-up", "chevron-down"), size=16),
                    spacing="2",
                    align="center",
                ),
                _estado_chip(row),  # mismo chip en móvil
                justify="between",
                width="100%",
                on_click=lambda: MobileRowState.toggle(row["id"]),
                cursor="pointer",
            ),
            rx.cond(
                is_expanded,
                rx.vstack(
                    rx.separator(size="4", margin_y="0.5em"),
                    rx.text(rx.text.span("Web: ", font_weight="bold"), row["web"], size="2"),
                    rx.cond(
                        Database.selected_category == "TOTAL GLOBAL",
                        rx.text(
                            rx.text.span("Grupo: ", font_weight="bold"),
                            row["grupo"],
                            size="2",
                        ),
                    ),
                    rx.text(
                        rx.text.span("Descripción: ", font_weight="bold"),
                        row["descripcion"],
                        size="2",
                    ),
                    spacing="1",
                    align_items="start",
                    width="100%",
                ),
            ),
            spacing="2",
            align_items="start",
        ),
        padding="1.2em",
        border_bottom=rx.color_mode_cond("1px solid #F1F5F9", "1px solid #334155"),
        width="100%",
    )


def get_pie_chart(ds, cat_name: str) -> rx.Component:
    return rx.recharts.pie_chart(
        rx.recharts.pie(
            data=ds,
            data_key="value",
            name_key="name",
            cx="50%",
            cy="50%",
            outer_radius="80%",
            on_click=lambda: Database.go_to_details(cat_name),
        ),
        rx.recharts.graphing_tooltip(),
        rx.recharts.legend(vertical_align="bottom"),
        width="100%",
        height=300,
    )
