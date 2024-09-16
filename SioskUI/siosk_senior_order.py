import flet as ft
from flet import View
from typing import Callable
import random
import time
import threading
import requests

def from_siosk_order(
        page: ft.Page, 
        store_getting_lowdata: Callable[[], None],
        data_arrange: list,
        drink_items: list,
        resource_path: str,
        ip_store: str,
        MENU: list,
        Menu: list,
    ):

    def background_function(column_content, containers): # Background Process Threading 등등
        page.add(column_content) # 에니매이션 처리
        animate_containers(containers) # 에니매이션 처리
        result = store_getting_lowdata(1, None) # 삽입되어진 값들을 호출 -> 키오스크
        names, amounts, prices, images = get_picture_link() # Picture Link를 받아오는 함수로써 이름, 양, 이미지 경로를 받아오는 역할을 한다.
        for beverage_index, beverage_val in enumerate(names):
            table_format = f"| {names[beverage_index]} | {amounts[beverage_index]} | {prices[beverage_index]} | {images[beverage_index]} |"
            # print(table_format)
        return names, amounts, prices, images

    def get_price_by_name(drink_name, drink_items): # 이름을 활용해서 이미지 경로 배열에서 이미지 경로를 추출
        for image, name_price, category in drink_items: # for 문으로 검사
            name, price = name_price.split("\n")  # 이름과 가격 분리
            if name == drink_name:
                return image
        return -1  

    def prettier_order_array(e):
        try:
            name = str(data_arrange[0][e]).split(' | ')[0]
            amount = str(data_arrange[0][e]).split(' | ')[1]
            price = str(data_arrange[0][e]).split(' | ')[2]
            return name, amount, price
        except IndexError:
            print("Please add least fake array valument")

    def get_picture_link():
        names = []
        amounts = []
        prices = []
        images = []
        for data_arrange_index, data_arrange_val in enumerate(data_arrange[0]):
            name, amount, price = prettier_order_array(data_arrange_index)
            image = get_price_by_name(name, drink_items=drink_items)
            names.append(name)
            amounts.append(amount)
            prices.append(price) 
            images.append(image)
        return names, amounts, prices, images

    def animate_containers(containers):
        for container in containers:
            page.add(container)  # 각 컨테이너를 페이지에 추가

        def toggle_height():
            while True:
                for container in containers:
                    new_height = random.randint(25, 100)
                    container.height = new_height
                    page.update()  # 이제 안전하게 업데이트 가능
                time.sleep(0.5)
        thread = threading.Thread(target=toggle_height)
        thread.daemon = True
        thread.start()

    containers = [
        ft.Container(
            bgcolor=ft.colors.BLACK,
            width=22.5,
            height=45,
            border_radius=ft.border_radius.all(30),
            animate=ft.Animation(600, "easeInOut"),
        ) for _ in range(4)
    ]

    centered_content = ft.Row(
        controls=ft.Container(
            containers,
            expand=True
        ),
        alignment=ft.MainAxisAlignment.END,
    )

    column_content = ft.Column(
        [
            ft.Container(
                centered_content,
            ),
        ],
    )
    
    names, amounts, prices, images = background_function(column_content=column_content, containers=containers)
    
    def total_amount():
        sum_data = []
        for beverage_sum_index, beverage_sum_val in enumerate(names):
            price_total = int(amounts[beverage_sum_index]) * int(str(prices[beverage_sum_index])[:-1])
            sum_data.append(price_total)
        return sum_data, sum(sum_data)

    def creating_containers():
        elements = []
        def update_amount(e, name, change):
            # print(name)
            # print(names.index(name))
            # print(amounts)
            amounts[int(names.index(name))] = int(amounts[int(names.index(name))]) + change
            page.update()

        for beverage_final_index, beverage_final_val in enumerate(names):
            
            element = ft.Container(
                ft.Row(
                    [
                        ft.Container(
                            ft.Image(
                                src=resource_path(f"{current_working_directory}/assets/images/{images[beverage_final_index]}"),
                                width=200,
                                height=200,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            width=150,
                            height=200,
                            border_radius=ft.border_radius.all(10),
                            shadow=ft.BoxShadow(
                                blur_radius=10,
                                offset=ft.Offset(0, 3)
                            ),
                            margin=ft.margin.only(left=20, bottom=10, top=5),
                            bgcolor='#ffffff',
                        ),
                        ft.Container(
                            ft.Column( 
                                [
                                    ft.Text(
                                        names[beverage_final_index],
                                        size=15,
                                        text_align=ft.TextAlign.CENTER,
                                        color=ft.colors.BLACK,
                                        font_family="NanumGothic"
                                    ),
                                    ft.Text(
                                        prices[beverage_final_index],
                                        size=15,
                                        text_align=ft.TextAlign.CENTER,
                                        color=ft.colors.BLACK,
                                        font_family="NanumGothic"
                                    ),
                                ],
                            ),
                            width=150,
                            margin=ft.margin.only(left=25)
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        ft.icons.REMOVE,
                                        icon_color=ft.colors.BLACK,
                                        # on_click=lambda e: update_amount(e, names[beverage_final_index], -1)
                                    ),
                                    ft.Text(
                                        value=amounts[int(names.index(names[beverage_final_index]))],
                                        size=10, 
                                        text_align=ft.TextAlign.CENTER, 
                                        color=ft.colors.BLACK,
                                        width=20,
                                        font_family="NanumGothic",
                                    ),
                                    ft.IconButton(
                                        ft.icons.ADD,
                                        icon_color=ft.colors.BLACK,
                                        # on_click=lambda e: update_amount(e, names[beverage_final_index], 1)
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            width=150,
                            border=ft.border.all(2.5, "#999999"),
                            border_radius=9
                        ),
                    ],
                    spacing=0
                )
            )
            elements.append(element)
        return elements
    
    money_list, money_sum = total_amount()
    money_sum = "{:,} dollar".format(money_sum)
    elements_array = creating_containers()
    text_color = "#55443d"
    text_weight = ft.FontWeight.W_900

    def connection(names, amounts, prices):
        # print(names)
        # print(amounts)
        # print(prices)
        requests.get(f"http://{ip_store[0]}:946", params={'names': str(names), 'amounts': str(amounts), 'prices': str(prices)})
        MENU.clear()
        Menu.clear()
        data_arrange.clear()
        page.go('/')

    return View(
        route="/from_general_order",
        controls=[
            ft.Container(
                ft.Column(
                    [
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Container(
                                        ft.Text(
                                            "Confirm an order.",
                                            size=17.5,
                                            text_align=ft.TextAlign.CENTER,
                                            color=ft.colors.BLACK,
                                            font_family="NanumGothic"
                                        ),
                                        ft.margin.only(left=20, right=200, top=50),
                                    ),
                                    ft.Container(
                                        ft.Row(
                                            controls=containers,
                                        ),
                                        margin=ft.margin.only(right=30),
                                        height=150
                                    ),
                                ]
                            ),
                            bgcolor=ft.colors.WHITE,
                        ),
                        ft.Container(
                            ft.Column(
                                controls=elements_array,
                                scroll='always',
                            ),
                            height=535,
                            bgcolor=ft.colors.WHITE,
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Container(
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    f"Sum:",
                                                    size=20,
                                                    color=text_color,
                                                    font_family="NanumGothic",
                                                    weight=text_weight,
                                                ),
                                                ft.Text(
                                                    money_sum,
                                                    size=20,
                                                    color=text_color,
                                                    font_family="NanumGothic",
                                                    weight=text_weight,
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        ),
                                        width=255,
                                        height=90,
                                        border=ft.border.all(2.5, color='#aba5a0'),
                                        border_radius=ft.border_radius.all(20),
                                        margin=ft.margin.only(left=5),
                                        padding=ft.padding.only(top=7.5, bottom=7.5, left=10, right=10)
                                    ),
                                    ft.Container(
                                        ft.Text(
                                            "Menu",
                                            size=20,
                                            color=text_color,
                                            font_family="NanumGothic",
                                            weight=text_weight,
                                        ),
                                        width=100,
                                        height=90,
                                        border=ft.border.all(2.5, color='#aba5a0'),
                                        border_radius=ft.border_radius.all(20),
                                        margin=ft.margin.only(left=5),
                                        padding=ft.padding.only(top=27.5, bottom=7.5, left=20, right=10),
                                        on_click=lambda _: page.go('/siosk_order')
                                    ),
                                    ft.Container(
                                        ft.Text(
                                            "Payment",
                                            size=20,
                                            color=text_color,
                                            font_family="NanumGothic",
                                            weight=text_weight,
                                        ),
                                        padding=ft.padding.only(top=30, left=31),
                                        width=145,
                                        height=90,
                                        border=None,
                                        border_radius=ft.border_radius.all(20),
                                        margin=ft.margin.only(left=5),
                                        bgcolor='#E6D5B8',
                                        on_click=lambda _: connection(names, amounts, prices)
                                    )
                                ]
                            ),
                            height=100,
                            alignment=ft.alignment.center,
                            margin=ft.margin.only(top=10, bottom=20)
                        )
                        # ft.Container(
                        #     ft.TextButton("/admininstrator_page", on_click=lambda _: page.go('/admininstrator_page')),
                        #     bgcolor=ft.colors.WHITE,
                        # ),
                    ],
                    spacing=0
                ),
                width=5000,
                height=5000,
                bgcolor=ft.colors.WHITE
            )
        ],
    )