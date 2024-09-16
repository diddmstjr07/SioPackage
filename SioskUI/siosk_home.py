import flet as ft
from flet import View
from Siosk.package.model import API
import threading

def build_home_view(
        page: ft.Page, 
        api: API,
        shadowed_img0, 
        shadowed_img1,
        width_ele,
    ):

    def ask_res():
        while True:
            A = api.detecting() # As Thread run, detecting my voice and convert as text to get response of question 
            if A == "결제페이지로 이동하겠습니다":
                print("Breaking")
                break
    
    def senior_mode(e):
        voice = threading.Thread(target=ask_res)
        voice.start()
        page.go('/siosk_order')
        voice.join()
    
    content0 = ft.Column(
        [
            ft.Container(
                shadowed_img0,
                alignment=ft.alignment.center,
                on_click=lambda _: page.go('/general_order')
            ),
            ft.Text(
                "Normal Order",
                size=20,
                text_align=ft.TextAlign.CENTER,
                color=ft.colors.BLACK,
                width=width_ele,
                font_family="NanumGothic"
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )

    content1 = ft.Column(
        [
            ft.Container(
                shadowed_img1,
                alignment=ft.alignment.center,
                on_click=senior_mode
            ),
            ft.Text(
                "Senior Order",
                size=20,
                text_align=ft.TextAlign.CENTER,
                color=ft.colors.BLACK,
                width=width_ele,
                font_family="NanumGothic"
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )

    return View(
        route="/",
        controls=[
            ft.Row(
                [
                    # ft.Container(
                    #     ft.TextButton("admin", on_click=lambda _:page.go("/admininstrator_page")),
                    # ),
                    ft.Container(
                        content0,
                        bgcolor='#fefcf6',
                        border=None,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                    ft.Container(
                        content1,
                        bgcolor='#e6d5b8',
                        border=None,
                        alignment=ft.alignment.center,
                        expand=True,
                    )
                ],
                spacing=0,
                expand=True,
            )
        ]
    )