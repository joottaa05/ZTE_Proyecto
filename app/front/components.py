import reflex as rx


def navbar() -> rx.Component:
    """Navegación profesional con rutas fijas."""
    return rx.flex(
        rx.link(
            "Inicio",
            href="/",
            color_scheme="blue",
            font_weight="bold",
        ),
        rx.link(
            "Servicios",
            href="/services",
            color_scheme="blue",
            font_weight="bold",
            margin_left="20px",
        ),
        rx.spacer(),
        rx.text(
            "ZTE Dashboard",
            color="#005C97",
            font_weight="bold"
        ),
        padding="1em 2em",
        width="100%",
        background="white",
        position="fixed",
        top="0",
        z_index="100",
        border_bottom="1px solid #E5E7EB",
    )


def card_grafica(titulo: str, grafica: rx.Component) -> rx.Component:
    """Tarjeta para los gráficos de rueda."""
    return rx.vstack(
        rx.text(
            titulo,
            font_weight="bold",
            color="#005C97"
        ),
        grafica,
        padding="1.5em",
        bg="white",
        border_radius="15px",
        box_shadow="0px 4px 20px rgba(0,0,0,0.05)",
        width="100%",
        align="center",
    )