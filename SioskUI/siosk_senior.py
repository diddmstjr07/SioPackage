
import flet as ft
from flet import View
import random
import time
import ast
import re
import threading
from auto.voice import play_wav
from typing import Callable
import os
import sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def build_siosk_order_view(
        page: ft.Page,
        drinks: list,
        MENU: list,
        Menu: list,
        drink_items: dict,
        key_data: list,
        store_getting_lowdata: Callable[[], None], 
        data_arrange: list,
        current_working_directory: str,
        sound,
    ):
    def close_dlg(e):
        dlg_modal.open = False
        page.update()
        
    dlg_modal = ft.AlertDialog(
        modal=True,
        bgcolor=ft.colors.WHITE,
        content=ft.Text(
            "메뉴를 적어도 한개 이상 선택해주세요", 
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

    menu_array = []
    amount_array = []
    file_path = "Siosk/package/log/logger.log"
    def checker():
        def counting():
            file = open(file_path, 'r', encoding='utf-8')
            line_count = 0
            try:
                for line in file:
                    line_count += 1
                return line_count
            finally:
                file.close()
        cnt_start = counting()
        while True:
            try:
                cnt = counting()
                if cnt != cnt_start:
                    with open(file_path, 'r', encoding='utf-8') as r:
                        lines = r.readlines()
                        if lines:
                            line = lines[-1]
                            classified, flag = line.split(" | ")
                            # print("Checker, New string detected: " + classified)
                            # print("Checker, New flag detected: " + flag)
                            try:
                                hint = update_standard(classified=classified, flag=flag)
                                if hint == False:
                                    break
                            except:
                                pass
                        else:
                            pass
                cnt_start = cnt
                time.sleep(1)
            except FileNotFoundError:
                break

    detecting = threading.Thread(target=checker)
    detecting.start()
    
    def update_standard(classified, flag): # Analyzing logged data + Adding to orderment array 
        if flag == '3':
            menu_array.append(classified)
        elif flag == '4':
            if classified == "one":
                amount_array.append("1")
            if classified == "two":
                amount_array.append("2")
            if classified == "three":
                amount_array.append("3")
            if classified == "four":
                amount_array.append("4")
            if classified == "five":
                amount_array.append("5")
            if classified == "six":
                amount_array.append("6")
        elif flag == '6':
            bool_data = classified
            if bool_data == 'True':
                print("\033[33m" + "LOG" + "\033[0m" + ":" + f"     Audio selected menu: {menu_array[0]}")
                print("\033[33m" + "LOG" + "\033[0m" + ":" + f"     Audio selected amount:  {amount_array[0]}")
                print("\033[33m" + "LOG" + "\033[0m" + ":" + f"     Audio selected bool data:  {bool_data}")
                automatic_updater(menu=menu_array[0], amount=amount_array[0])
                menu_array.clear()
                amount_array.clear()
            elif bool_data == 'False':
                print("\033[33m" + "LOG" + "\033[0m" + ":" + f"     Order Canceled: {bool_data}")
        elif flag == '7':
            submit_audio_version()
            with open('Siosk/package/log/logger.log', 'w', encoding='utf-8') as file:
                pass
            return False
        elif flag == 'Gemini':
            pass

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
        ("Recommand", rnd),
        ("Coffee", lambda: "Coffee"),
        ("Smoothe\nFrappe", lambda: "Smoothe"),
        ("Beverage", lambda: "Beverage"),
        ("Ade", lambda: "Ade"),
        ("Tea", lambda: "Tea"),
        ("Dessert", None)
    ]

    text_array = [
        ft.Container(
            ft.Text(
                text,
                size="12.5",
                color=text_color,
                font_family="NanumGothic",
                weight=text_weight
            ),
            ft.padding.only(bottom=35),
            on_click=lambda e, key=key: (orderment.scroll_to(key=key(), duration=1000) if key else None)
        ) for text, key in text_tuples
    ]

    text_column = ft.Column(
        [ft.Container(text, alignment=ft.alignment.center) for text in text_array],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    def start_menu_click(e):
        MENU.clear()
        Menu.clear()
        page.go('/')
    
    display = ft.Container(
        ft.Column(
            [
                text_column,
                ft.Container(
                    ft.Column(
                        [
                            ft.Container(
                                ft.Icon(name=ft.icons.HOME_ROUNDED, size=30, color=text_color),
                                alignment=ft.alignment.center,
                                on_click=start_menu_click
                            ),
                            ft.Container(
                                ft.Text(
                                    "Home",
                                    size=12.5,
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
        bgcolor='#e6d5b8',
        height=1500,
        expand=True
    )

    def fee_sum_data():
        fee = 0
        for menu in range(len(Menu)):
            # print(MENU[menu])
            select_drink = ast.literal_eval(str(Menu[menu])[5:])['value']
            # print(select_drink)
            result = str(select_drink).split(' ')[-1][0]
            fee += int(result)
        return fee
    
    def fee_sum_data_auto():
        fee = 0
        for menu in range(len(Menu)):
            # print(MENU[menu])
            select_drink = ast.literal_eval(str(Menu[menu])[5:])['value']
            # print(select_drink)
            result = str(select_drink).split(' ')[-1][0]
            fee += int(result)
        # print(fee)
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
                pattern = r"(.+)\s(\d+)\$"
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
        store_getting_lowdata(0, amount_menus) # 데이터를 삽입하도록 호출 -> 시오스크
        return amount_menus
    
    def check_duplicated_auto():
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
                pattern = r"(.+)\s(\d+)\$"
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
        store_getting_lowdata(0, amount_menus) # 데이터를 삽입하도록 호출 -> 시오스크
        return amount_menus
    
    def on_click_handler(e):
        click(e.control)
        container = e.control.data # 클릭한 부분의 Container 데이터 가지고 오기
        datas = str(container).split('\n') # 줄 나눔하기 메뉴랑 가격이랑 다른줄로 나누어져 있기때문에
        texture = "" # 가격이랑 상품명을 한줄로 만들어서 textture 변수에 문자열로 저장해주기
        texture = f"{datas[0]} {str(datas[1]).split(' ')[0]}$"
        order_menu = ft.Text(
            value=texture,
            size="15",
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
                size="15",
                color=text_color,
                font_family="NanumGothic",
                weight=text_weight,
                key=data_str
            )
            MENU.append(list_result)
            order_list.update()
        sum_dataa = ft.Text(
            value="  " + str(total) + " dollar",
            size="15",
            color=text_color,
            font_family="NanumGothic",
            weight=text_weight,
        )
        sum.controls = [sum_dataa] 
        sum.update()
        # print(f'Clicked on: {container}')
    
    def extracting_fee(drink_name):
        drink_prices = {item[1].split('\n')[0]: item[1].split('\n')[1] for item in drink_items}
        expanded_drink_prices = {}
        for key, value in drink_prices.items():
            expanded_drink_prices[key] = value
            expanded_drink_prices[key.replace(" ", "")] = (key, value)

        # 음료 이름으로 가격을 검색
        price = drink_prices.get(drink_name)
        if price:
            return drink_name, price
        else:
            price_re = expanded_drink_prices.get(drink_name)
            if price_re:
                return price_re
            else:
                return None

    def automatic_updater(menu, amount):
        drink_name, price = extracting_fee(menu)
        # print(price)
        # print(menu)
        texture = f"{drink_name} {price.split(' ')[0]}$" 
        '''
        text {'value': '아이스 아메리카노 4 dollar ', 'fontfamily': 'NanumGothic', 'size': '30', 'weight': 'w900', 'color': '#55443d'} -> 일반 클릭
        text {'value': '아이스 아메리카노 4 dollar', 'fontfamily': 'NanumGothic', 'size': 15, 'weight': 'w900', 'color': '#55443d'} -> 음성 클릭
        '''
        for _ in range(int(amount)):
            order_menu = ft.Text(
                value=texture,
                size="15",
                color=text_color,
                font_family="NanumGothic",
                weight=text_weight
            )
            Menu.append(order_menu)
        # print(Menu)
        total = fee_sum_data_auto()
        amount_orders = check_duplicated_auto()
        order_list.clean()
        for amount_order in range(len(amount_orders)):
            data_str = str(amount_orders[amount_order]).split(" | ")[0]
            data_int = str(amount_orders[amount_order]).split(" | ")[1]
            data_price = str(amount_orders[amount_order]).split(" | ")[2]
            # print(data_str)
            list_result = ft.Text(
                value=data_str + " " + data_price + f" x {data_int}",
                size="15",
                color=text_color,
                font_family="NanumGothic",
                weight=text_weight,
                key=data_str
            )
            MENU.append(list_result)
            order_list.update()
        sum_dataa = ft.Text(
            value=" " + str(total) + " dollar",
            size="15",
            color=text_color,
            font_family="NanumGothic",
            weight=text_weight,
        )
        sum.controls = [sum_dataa] 
        sum.update()
        play_wav(sound)
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
            
    def submit(e): # e 값을 받아서 open_dlg_model을 호출하자 -> Siosk에 대해서
        if len(data_arrange) != 0: # data_arrange는 최종적으로 메뉴를 포함하고 있는 배열의 정보이다. 
            page.go('/from_siosk_order') # 이부분은 결제하기를 눌렀을때 나오는 페이지를 뜻함
        elif len(data_arrange) == 0:
            open_dlg_modal(e) # 0개인 경우에는 alert함수 호출

    def submit_audio_version(): # e 값을 받아서 open_dlg_model을 호출하자 -> Siosk에 대해서
        page.go('/from_siosk_order') # 이부분은 결제하기를 눌렀을때 나오는 페이지를 뜻함
        play_wav(sound)

    def create_menu_item(image, text, key):
        container = ft.Container(
            ft.Image(
                src=resource_path(f"{current_working_directory}/assets/images/{image}"),
                width=375,
                height=375,
            ),
            padding=ft.padding.only(top=10),
            margin=ft.margin.only(top=25, left=15),
            alignment=ft.alignment.top_left,
            width=187.5,
            height=275,
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
                    size=12.5,
                    color=text_color,
                    font_family="NanumGothic",
                    weight=text_weight,
                    text_align=ft.alignment.top_left
                ),
                margin=ft.margin.only(top=5, left=12.5)
            )
        ])

    rows = []
    for i in range(0, len(drink_items), 2):
        menu_cols = [create_menu_item(*item) for item in drink_items[i:i+2]]
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

    submit_button_click_handler = submit

    order_box = ft.Container(
        ft.Row(
            [
                ft.Container(
                    row_sum,
                    width=305,
                    height=90,
                    border=ft.border.all(4, color='#aba5a0'),
                    border_radius=ft.border_radius.all(20),
                    margin=ft.margin.only(left=5),
                    padding=ft.padding.only(top=7.5, bottom=7.5, left=10, right=10)
                ),
                ft.Container(
                    ft.Text(
                        "Payment",
                        size=20,
                        color=text_color,
                        font_family="NanumGothic",
                        weight=text_weight,
                    ),
                    padding=ft.padding.only(top=30, left=13),
                    width=110,
                    height=160,
                    border=None,
                    border_radius=ft.border_radius.all(20),
                    margin=ft.margin.only(right=10, bottom=7),
                    bgcolor='#E6D5B8',
                    on_click=submit # 메뉴가 있는지 확인하는 함수에 있어서 e를 받기 위해서는 함수 그대로를 호출해주어야한다.
                )
            ]
        ),
        height=100,
        alignment=ft.alignment.center
    )

    orderment = ft.Column(
        rows,
        scroll='always',
        expand=True
    )

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
                margin=ft.margin.only(right=30, bottom=5),
                expand=True
            ),
        ],
    )
    
    page.add(column_content)
    animate_containers(containers)
    return View(
        route="/general_order",
        controls=[
            ft.Row(
                [
                    display,
                    ft.Container(
                        ft.Column(
                            [
                                ft.Container(
                                    ft.Row(
                                        controls=containers,
                                        alignment=ft.MainAxisAlignment.END,
                                    ),
                                    margin=ft.margin.only(right=30),
                                    height=115,
                                ),
                                orderment,
                                order_box
                            ],
                        ),
                        bgcolor='#fefcf6',
                        border=None,
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(left=10),
                        width=450,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        ],
    )