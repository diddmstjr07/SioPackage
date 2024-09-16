import flet as ft
import requests
import threading
import time
import random
import os
from auto.delete import delete_dot_underscore_files

current_working_directory = os.getcwd()
# print(current_working_directory)

def getting_ip():
    url = "http://checkip.dyndns.org"
    result = requests.get(url)
    data = str(result.text).split("<body>")[1].split(":")[1].split("</body>")[0][1:]
    return data

def animate_containers(page, containers):
    def toggle_height():
        while True:
            for container in containers:
                if container.height >= 100:
                    random_integer = random.randint(50, 100)
                    container.height = random_integer
                elif container.height < 100:
                    random_integer = random.randint(100, 200)
                    container.height = random_integer
                container.update()
            time.sleep(0.5)
    thread = threading.Thread(target=toggle_height)
    thread.daemon = True
    thread.start()

def falling(beverage, container):
    def falling_shape():
        random_angle = random.randint(11, 99)
        ne_po = random.randint(0, 1)
        ne_po = "-" if ne_po == 0 else "+"
        random_float = float(f"{ne_po}0." + str(random_angle))
        bottom_height = 600
        while bottom_height > 0:
            beverage.rotate = ft.Rotate(angle=random_float, alignment=ft.alignment.center_left)
            container.margin = ft.margin.only(bottom=bottom_height, left=130)
            beverage.update()
            random_float += 0.02
            bottom_height = bottom_height - 10
            container.update()
            # print(bottom_height)
            time.sleep(0.01)
    thread = threading.Thread(target=falling_shape)
    thread.daemon = True
    thread.start()
    beverage.visible = True
    beverage.update()
    thread.join()
    beverage.visible = False
    beverage.update()

def creating(kind, page):
    if kind == "cold":
        coffee = ft.Image(
            src=f"{current_working_directory}/assets/ice_coffee.png",
            width=50,
            height=50,
            visible=False,
            expand=True,
        )
    else:
        coffee = ft.Image(
            src=f"{current_working_directory}/assets/hot_coffee.png",
            width=50,
            height=50,
            visible=False,
            expand=True,
        )
    container = ft.Container(
        content=coffee,
        margin=ft.margin.only(bottom=600, left=130)
    )
    page.add(container)  # Add the container to the page first
    falling(coffee, container)

def main(page: ft.Page):
    page.window_width = 400 
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT
    page.update()

    ip_text = ft.Text(
        getting_ip(),
        size=10,
        color=ft.colors.BLACK,
        weight=ft.FontWeight.BOLD,
        italic=True
    )

    containers = [
        ft.Container(
            bgcolor=ft.colors.BLACK,
            width=50,
            height=100,
            border_radius=ft.border_radius.all(30),
            animate=ft.Animation(600, "easeInOut")
        ) for _ in range(4)
    ]

    centered_content = ft.Row(
        controls=containers,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    floating_action_button_red = ft.FloatingActionButton(
        icon=ft.icons.ADD, 
        bgcolor=ft.colors.RED_ACCENT_100, 
        on_click=lambda e: creating("red", page)
    )
    floating_action_button_blue = ft.FloatingActionButton(
        icon=ft.icons.ADD, 
        bgcolor=ft.colors.BLUE_100, 
        on_click=lambda e: creating("cold", page) 
    )

    column_content = ft.Column(
        [
            ft.Container(height=200),
            centered_content,
            ft.Container(expand=True),
        ],
        expand=True,
    )

    floating_action_buttons = ft.Column(
        [   
            ft.Container(height=20),     
            floating_action_button_red,
            ft.Container(height=1),
            floating_action_button_blue
        ],
        expand=True,
    )

    page.add(
        ft.Stack(
            [
                column_content,
                floating_action_buttons,
                ip_text
            ],
            expand=True,
        )
    )
    animate_containers(page, containers)

if __name__ == "__main__":
    delete_dot_underscore_files()
    ft.app(target=main)