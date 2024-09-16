import flet as ft
from flet import View

def from_general_order():
    return View(
        route="/from_siosk_order",
        controls=[
            ft.Container(
                ft.Text("Hello Fucking World")
            ),
            ft.Container(
                ft.TextButton("movement to Administrator Page", on_click=lambda _:page.go("/admininstrator_page"))
            )
        ]
    )