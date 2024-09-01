import reflex as rx


def index() -> rx.Component:
    return rx.container(
        rx.box(
            "Homepage",
            text_align="right"
        ),
        rx.box(
            "Hello world",
            text_align="left"
        ),
    )