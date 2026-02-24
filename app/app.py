import reflex as rx
from app.front.components import (
    navbar, 
    card_grafica
)
from app.back.database import (
    State, 
    get_pie
)


def index() -> rx.Component:
    """Página de bienvenida."""
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                rx.heading(
                    "ZTE",
                    size="9",
                    style={
                        "color": "#005C97",
                        "font_size": "10vw",
                    },
                ),
            ),
            width="100%",
            height="100vh",
        ),
    )


def services() -> rx.Component:
    """Panel con las 4 ruletas interactivas."""
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading(
                    "Panel de Control", 
                    margin_top="4em"
                ),
                rx.grid(
                    card_grafica(
                        "CAT N1", 
                        get_pie(State.c_n1, "#3B82F6", "CAT N1")
                    ),
                    card_grafica(
                        "CAT MASIVO", 
                        get_pie(State.c_mas, "#10B981", "CAT MASIVO")
                    ),
                    card_grafica(
                        "CAT N2 VOZ", 
                        get_pie(State.c_voz, "#F59E0B", "CAT N2 VOZ")
                    ),
                    card_grafica(
                        "CAT N2 DATOS", 
                        get_pie(State.c_dat, "#EF4444", "CAT N2 DATOS")
                    ),
                    columns=rx.breakpoints(initial="1", sm="2"),
                    spacing="6",
                    width="100%",
                ),
                padding_bottom="5em",
            ),
        ),
        on_mount=State.load_data,
    )


def details() -> rx.Component:
    """Página de tabla filtrada."""
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading(
                    f"Detalle: {State.selected_category}", 
                    margin_top="4em"
                ),
                rx.input(
                    placeholder="Escribe para buscar...",
                    on_change=State.set_search_text,
                    width="100%",
                ),
                rx.data_table(
                    data=State.filtered_rows,
                    columns=[
                        "Grupo", 
                        "Empresa", 
                        "Servicio", 
                        "Prioridad"
                    ],
                    pagination=True,
                ),
                rx.button(
                    "Cerrar", 
                    on_click=rx.redirect("/services")
                ),
                width="100%",
                spacing="4",
            ),
        ),
    )


app = rx.App()
app.add_page(index, route="/")
app.add_page(services, route="/services")
app.add_page(details, route="/details")