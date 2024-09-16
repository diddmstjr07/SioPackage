
import flet as ft
from flet import View

def administrator_page(
        page: ft.Page,
        data_arrange: list,
        MENU: list,
        Menu: list
    ):
    def initing():
        print("\nData Initing -> Client Pressed home button")
        print("------------------------------------------")
        print(data_arrange)
        print("------------------------------------------\n")
        MENU.clear()
        Menu.clear()
        data_arrange.clear()

    def adding(e):
        try:
            amount = str(data_arrange[0][0]).split(' | ')[1]
            data_arrange.clear()
            temp_fake_array = []
            temp_fake_array.append(f'카페 모카 | {int(amount) + 1} | 4 dollar')
            data_arrange.append(temp_fake_array)
            print("data insulting")
            print(data_arrange)
        except IndexError:
            temp_fake_array = []
            temp_fake_array.append(f'카페 모카 | {e} | 4 dollar')
            data_arrange.append(temp_fake_array)
            print("data insulting")
            print(data_arrange)

    return View(
        route="/admininstrator_page",
        controls=[
            ft.Container(
                height=500
            ),
            ft.Container(
                ft.TextButton("/", on_click=lambda _:page.go("/")) # lamba를 쓰는 이유는 즉석 Function을 만들어내기 위함에 있음, 즉시 함수를 생성하여 Onclick 넣어주기
            ),
            ft.Container(
                ft.TextButton("/general_order", on_click=lambda _:page.go("/general_order"))
            ),
            ft.Container(
                ft.TextButton("/siosk_order", on_click=lambda _:page.go("/siosk_order"))
            ),
            ft.Container(
                ft.TextButton("/from_general_order", on_click=lambda _:page.go("/from_general_order"))
            ),
            ft.Container(
                ft.TextButton("/from_siosk_order", on_click=lambda _:page.go("/from_siosk_order"))
            ),
            ft.Container(
                ft.TextButton("Initing", on_click=lambda _: initing())
            ),
            ft.Container(
                ft.TextButton("Adding", on_click=lambda _: adding(1))
            )
        ]
    )
