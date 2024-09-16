import flet as ft
from flet import View
from typing import Callable
import random
import ast
import re
import time
import os
import sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def build_general_order_view(
        page: ft.Page, 
        drinks: list, 
        MENU: list, 
        Menu: list, 
        key_data: list, 
        data_arrange: list, 
        store_getting_lowdata: Callable[[], None],
        drink_items: dict,
        current_working_directory: str
    ):

    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    dlg_modal = ft.AlertDialog(
        modal=True,
        bgcolor=ft.colors.WHITE,
        content=ft.Text(
            "Please select more than one menu", 
            color='#55443d',
            font_family="NanumGothic",
        ),
        actions=[
            ft.TextButton(
                "확인", 
                on_click=close_dlg,
                style=ft.ButtonStyle(
                    color=ft.colors.BLACK,
                )
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()
    
    def rnd():
        for _ in range(len(drinks)):
            key_value = drinks[random.randint(0, len(drinks) - 1)]
            return key_value
    text_size = 7.5
    text_color = "#55443d"
    text_weight = ft.FontWeight.W_900

    text_tuples = [
        ("추천", rnd),
        ("커피", lambda: "Coffee"),
        ("스무디\n프라페", lambda: "Smoothe"),
        ("음료", lambda: "Beverage"),
        ("에이드", lambda: "Ade"),
        ("차(Tea)", lambda: "Tea"),
        ("디저트", None)
    ]

    text_array = [
        ft.Container(
            ft.Text(
                text,
                size="10",
                color=text_color,
                font_family="NanumGothic",
                weight=text_weight
            ),
            ft.padding.only(bottom=30),
            on_click=(lambda e, key=key: orderment.scroll_to(key=key(), duration=1000) if key else None)
        ) for text, key in text_tuples
    ]

    text_column = ft.Column(
        [ft.Container(text, alignment=ft.alignment.center) for text in text_array],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    def start_menu_click(e):
        # print("\nData Initing -> Client Pressed home button")
        # print("------------------------------------------")
        # print(data_arrange)
        # print("------------------------------------------\n")
        MENU.clear()
        Menu.clear()
        key_data.clear()
        data_arrange.clear()
        page.go('/')
    
    display = ft.Container(
        ft.Column(
            [
                text_column,
                ft.Container(
                    ft.Column(
                        [
                            ft.Container(
                                ft.Icon(name=ft.icons.HOME_ROUNDED, size=20, color=text_color),
                                alignment=ft.alignment.center,
                                on_click=start_menu_click
                            ),
                            ft.Container(
                                ft.Text(
                                    "Home",
                                    size=10,
                                    color=text_color,
                                    font_family="NanumGothic",
                                    weight=text_weight
                                ),
                                alignment=ft.alignment.center,
                                padding=ft.padding.only(bottom=15)
                            )
                        ]
                    ),
                    alignment=ft.alignment.center,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        ),
        bgcolor='#FFD700',
        height=1500,
        expand=True
    )

    def fee_sum_data():
        fee = 0
        for menu in range(len(Menu)):
            # print(MENU[menu])
            select_drink = ast.literal_eval(str(Menu[menu])[5:])['value']
            result = str(select_drink).split(' ')[-2]
            fee += int(result[:-1])
        return fee
    
    def check_duplicated():
        amount_menus = []  
        for menu in range(len(Menu)):
            updated = ""                                                                                                                                     
            for drink_item in drink_items:
                select_drink = ast.literal_eval(str(Menu[menu])[5:])['value']
                data = str(drink_item[1]).split("\n")[0]
                if str(data).split(' ')[0] == str(data).split(' ')[-1]:
                    result = str(data).split(' ')[0] 
                else:
                    result = str(data).split(' ')[0] + " " + str(data).split(' ')[-1]
                pattern = r"(.+)\s(\d+) dollar"
                match = re.match(pattern, str(select_drink))
                if match:
                    item = match.group(1)
                    if result == item:
                        for index, val in enumerate(amount_menus):
                            raw_data = str(val).split(" | ")[0]
                            cal_data = str(val).split(" | ")[1]
                            if raw_data == item:
                                amount_menus[index] = f"{item} | {int(cal_data) + 1} | {str(match.group(0).split(item)[1])[1:]}"
                                key_data.append(item)
                                updated += "1"
                        if updated == "":
                            menu_data = f"{item} | 1 | {str(match.group(0).split(item)[1])[1:]}"
                            amount_menus.append(menu_data)
        # print(amount_menus)
        store_getting_lowdata(0, amount_menus) # 데이터를 삽입하도록 호출
        return amount_menus

    def on_click_handler(e):
        click(e.control)
        container = e.control.data # 클릭한 부분의 Container 데이터 가지고 오기
        datas = str(container).split('\n') # 줄 나눔하기 메뉴랑 가격이랑 다른줄로 나누어져 있기때문에
        texture = "" # 가격이랑 상품명을 한줄로 만들어서 textture 변수에 문자열로 저장해주기
        for data in range(len(datas)):
            texture += str(datas[data] + " ")
        order_menu = ft.Text(
            value=texture,
            size=text_size,
            color=text_color,
            font_family="NanumGothic",
            weight=text_weight
        ) # flet Text Container 만들어주기 여기에는 지금 가격이랑 상품명을 한줄로 나타내줌
        Menu.append(order_menu) # Menu 항목에 append 해주기
        total = fee_sum_data() # 총 금액 변수에 저장
        amount_orders = check_duplicated() # 겹친것이나 여러가지 요소들을 처리해주기
        order_list.clean() # 리스트 초기화하기
        for amount_order in range(len(amount_orders)):
            data_str = str(amount_orders[amount_order]).split(" | ")[0]
            data_int = str(amount_orders[amount_order]).split(" | ")[1]
            data_price = str(amount_orders[amount_order]).split(" | ")[2]
            # print(data_str)
            list_result = ft.Text(
                value=data_str + " " + data_price + f" x {data_int}",
                size=text_size,
                color=text_color,
                font_family="NanumGothic",
                weight=text_weight,
                key=data_str
            )
            MENU.append(list_result)
            order_list.update()
        sum_dataa = ft.Text(
            value="  " + str(total) + " dollar",
            size=text_size,
            color=text_color,
            font_family="NanumGothic",
            weight=text_weight,
        )
        sum.controls = [sum_dataa] 
        sum.update()
        # print(f'Clicked on: {container}')

    def click(env):
        animations = [
            ft.Offset(0, 2.0), ft.Offset(0, 1.9), ft.Offset(0, 1.8),
            ft.Offset(0, 1.7), ft.Offset(0, 1.6), ft.Offset(0, 1.5),
            ft.Offset(0, 1.4), ft.Offset(0, 1.3), ft.Offset(0, 1.2),
            ft.Offset(0, 1.1), ft.Offset(0, 1.0), ft.Offset(0, 0.9),
            ft.Offset(0, 0.8), ft.Offset(0, 0.7), ft.Offset(0, 0.6),
            ft.Offset(0, 0.5), ft.Offset(0, 0.4), ft.Offset(0, 0.3),
            ft.Offset(0, 0.2), ft.Offset(0, 0.1), ft.Offset(0, 0.0),
            ft.Offset(0, 0.1), ft.Offset(0, 0.2), ft.Offset(0, 0.3),
            ft.Offset(0, 0.4), ft.Offset(0, 0.5), ft.Offset(0, 0.6),
            ft.Offset(0, 0.7), ft.Offset(0, 0.8), ft.Offset(0, 0.9),
            ft.Offset(0, 1.0), ft.Offset(0, 1.1), ft.Offset(0, 1.2),
            ft.Offset(0, 1.3), ft.Offset(0, 1.4), ft.Offset(0, 1.5),
            ft.Offset(0, 1.6), ft.Offset(0, 1.7), ft.Offset(0, 1.8),
            ft.Offset(0, 1.9), ft.Offset(0, 2.0)
        ]
        for offset in animations:
            env.shadow = ft.BoxShadow(blur_radius=10, offset=offset)
            env.update()
            time.sleep(0.005)

    def submit(e): # e 값을 받아서 open_dlg_model을 호출하자 -> Kiosk에 대해서
        if len(data_arrange) != 0: # data_arrange는 최종적으로 메뉴를 포함하고 있는 배열의 정보이다. 
            # page.go('/from_general_order') # 이부분은 결제하기를 눌렀을때 나오는 페이지를 뜻함
            pass
        elif len(data_arrange) == 0:
            open_dlg_modal(e) # 0개인 경우에는 alert함수 호출

    def create_menu_item(image, text, key):
        container = ft.Container(
            ft.Image(
                src=resource_path(f"{current_working_directory}/assets/images/{image}"),
                width=180,
                height=180,
            ),
            padding=ft.padding.only(top=10),
            margin=ft.margin.only(top=10, left=10.5),
            alignment=ft.alignment.top_left,
            width=90,
            height=132,
            bgcolor='#ffffff',
            border_radius=ft.border_radius.all(10),
            shadow=ft.BoxShadow(
                blur_radius=10,
                offset=ft.Offset(0, 3)
            ),
            on_click=on_click_handler,
            key=key if key else None
        )
        container.data = text  
        return ft.Column([
            container,
            ft.Container(
                ft.Text(
                    text,
                    size=7.5,
                    color=text_color,
                    font_family="NanumGothic",
                    weight=text_weight,
                    text_align=ft.alignment.top_left
                ),
                margin=ft.margin.only(left=12.5)
            )
        ])

    rows = []
    for i in range(0, len(drink_items), 4):
        menu_cols = [create_menu_item(*item) for item in drink_items[i:i+4]]
        rows.append(ft.Row(menu_cols))

    sum = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
    )

    order_list = ft.Column(
        MENU,
        scroll='always',
        auto_scroll=True,
        expand=True,
        # key를 활용해서 key 이동이 되어지도록
    )

    row_sum = ft.Row(
        [
            order_list,
            sum
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    order_box = ft.Container(
        ft.Row(
            [
                ft.Container(
                    row_sum,
                    width=640,
                    height=100,
                    border=ft.border.all(4, color='#aba5a0'),
                    border_radius=ft.border_radius.all(10),
                    margin=ft.margin.only(left=5),
                    padding=ft.padding.only(top=7.5, bottom=7.5, left=10, right=10)
                ),
                ft.Container(
                    ft.Text(
                        "Payment",
                        size=12.5,
                        color=text_color,
                        font_family="NanumGothic",
                        weight=text_weight,
                    ),
                    padding=ft.padding.only(top=14, left=22),
                    width=90,
                    height=50,
                    border=None,
                    border_radius=ft.border_radius.all(10),
                    margin=ft.margin.only(right=10),
                    bgcolor='#FFD700',
                    on_click=submit # 메뉴가 있는지 확인하는 함수에 있어서 e를 받기 위해서는 함수 그대로를 호출해주어야한다.
                )
            ]
        ),
        height=55,
        alignment=ft.alignment.center
    )

    orderment = ft.Column(
        rows,
        scroll='always',
        expand=True
    )

    return View(
        route="/general_order",
        controls=[
            ft.Row(
                [
                    display,
                    ft.Container(
                        ft.Column(
                            [
                                ft.Container(height=10),
                                orderment,
                                order_box
                            ],
                        ),
                        bgcolor='#fefcf6',
                        border=None,
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(left=20),
                        width=470
                    ),
                ],
                spacing=0,
                expand=True,
            )
        ]

    )