import reflex as rx
from homepage import index


config = rx.Config(
    app_name="reflex_app",
)

app = rx.App()
app.add_page(index)
