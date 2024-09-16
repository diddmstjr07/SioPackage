import flet as ft
from flet import View, RouteChangeEvent
import os
import requests
import Siosk.package.download as download
from Siosk.package.TTS import TextToSpeech
from Siosk.package.scan import find_process_by_port_Voice
from SioskUI.siosk_home import build_home_view
from SioskUI.siosk_general import build_general_order_view
from SioskUI.siosk_senior import build_siosk_order_view
from SioskUI.siosk_developer import administrator_page
from SioskUI.siosk_general_order import from_general_order
from SioskUI.siosk_senior_order import from_siosk_order
from Siosk.package.model import API
import sys
import requests
import os  

current_working_directory = os.path.abspath(".") + "/SioskUI"
drinks = ["Coffee", "Smoothe", "Beverage", "Tea", "Ade"]
ip_store = []

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class UI:
    def __init__(self) -> None:
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Establish Connection with Server...")
        try:
            res = requests.get(f"http://127.0.0.1:9460/api?token=SioskKioskFixedTokenVerifyingTokenData&ques=안녕", verify=False)
        except requests.exceptions.ConnectionError:
            print("\033[1;91m" + "ERROR" + "\033[0m" + ":" + f"    Is your Server is Waken??")
            os._exit(0)
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     {res}")
        save_dir = "Siosk/package/" # Conversation.json이 있는지 확인하고 없으면 서버에서 다운로드
        download.download_file(file="conversation_en.json", save_dir=save_dir) # Conversation.json이 있는지 확인하고 없으면 서버에서 다운로드
        self.TextToSpeech = TextToSpeech()
        self.sound = "assets/audio/click.wav"
        ip_address = "127.0.0.1"
        ip_store.append(ip_address)

        if ip_address == "127.0.0.1":
            bool_data = find_process_by_port_Voice(9460)
            if bool_data == True:
                self.api = API(
                    token="SioskKioskFixedTokenVerifyingTokenData",
                    url="http://" + ip_address
                )
            elif bool_data == False:
                self.api = API(
                    token="SioskKioskFixedTokenVerifyingTokenData",
                    url="http://127.0.0.1"
                )
        else:
            self.api = API(
                token="SioskKioskFixedTokenVerifyingTokenData",
                url="http://" + ip_address
            ) 
        self.api.preparing() # Mic selection, storing class elements declaring as instant variable

    def main(self, page: ft.Page):
        '''
        Kiosk, Siosk UI Version
        '''
        MENU = []
        Menu = []
        key_data = []
        data_arrange = []
        drink_items = [ 
            (f"coffee/iceamericano.png", "iced Americano\n4 dollar", "Coffee"),
            (f"coffee/kapuchino.png", "hot Americano\n4 dollar", "Coffee"),
            (f"coffee/younyu_latte.png", "sweetened latte\n4 dollar", None),
            (f"coffee/kapuchino.png", "cappuccino\n4 dollar", None),
            (f"coffee/Hazelnut_Latte.png", "hazelnut latte\n4 dollar", None),
            (f"coffee/Hazelnut_Americano.png", "hazelnut Americano\n4 dollar", None),
            (f"coffee/Coldbrew_Latte.png", "cold brew latte\n4 dollar", None),
            (f"coffee/cold_brew_original.png", "cold brew\n4 dollar", None),
            (f"coffee/Caramel_Macchiato.png", "caramel macchiato\n4 dollar", None),
            (f"coffee/Caffe_Mocha.png", "cafe mocha\n4 dollar", None),
            (f"frappe/Mint_Frappe.png", "mint frappe\n4 dollar", None),
            (f"frappe/Green_Tea_Frappe.png", "green tea frappe\n4 dollar", "Smoothe"),
            (f"frappe/Unicorn_Frappe.png", "unicorn frappe\n4 dollar", None),
            (f"pongcrush/Banana_Pongcrush.png", "banana funk crush\n4 dollar", "Beverage"),
            (f"pongcrush/Chocolate_Honey_Pong_Crush.png", "chocolate honey funk crush\n4 dollar", None),
            (f"pongcrush/Choux_Cream_Honey_Pong_Crush.png", "cream honey funk crush\n4 dollar", None),
            (f"pongcrush/Plain_Pongcrush.png", "plain funk crush\n4 dollar", None),
            (f"pongcrush/Strawberry_pongcrush.png", "strawberry funk crush\n4 dollar", None),
            (f"pongcrush/Strawberry_Cookie_Frappe.png", "strawberry cookie frappe\n4 dollar", None),
            (f"smoothie/Mango_Yogurt_Smoothie.png", "mango yogurt smoothie\n4 dollar", None),
            (f"smoothie/Plain_Yogurt_Smoothie.png", "plain yogurt smoothie\n4 dollar", None),
            (f"smoothie/Strawberry_Yogurt_Smoothie.png", "strawberry yogurt smoothie\n4 dollar", None),
            (f"ade/Blue_Lemon_Ade.png", "blue lemon ade\n4 dollar", "Ade"),
            (f"ade/Cherry_Coke.png", "cherry coke\n4 dollar", None),
            (f"ade/Grapefruit_Ade.png", "grapefruit ade\n4 dollar", None),
            (f"ade/Lemon_Ade.png", "lemon ade\n4 dollar", None),
            (f"ade/Lime_Mojito.png", "lime mojito\n4 dollar", None),
            (f"ade/MEGA_Ade.png", "mega ade\n4 dollar", None),
            (f"tea/Hot_lemon_tea.png", "lemon tea\n4 dollar", None),
            (f"tea/Applecitron_Tea.png", "apple yuzu tea\n4 dollar", "Tea"),
            (f"tea/Chamomile.png", "chamomile tea\n4 dollar", None),
            (f"tea/Green_Tea.png", "green tea\n4 dollar", None),
            (f"tea/Earl_Grey.png", "Earl Grey\n4 dollar", None),
            (f"tea/Hot_Grapefruit_tea.png", "grapefruit tea\n4 dollar", None),
        ]

        page.title = "시오스크"
        page.window_width = 570
        page.window_height = 850
        # route_history = []

        page.fonts = {
            "NanumGothic": "SioskUI/assets/fonts/NanumGothic-Bold.ttf"
        }

        img0 = ft.Image(
            src=resource_path(resource_path(f"{current_working_directory}/assets/images/logo/general.png")),
            width=150,
            height=150,
            fit=ft.ImageFit.CONTAIN,
        )

        shadowed_img0 = ft.Container(
            img0,
            padding=5
        )
        width_ele = page.window_width
        height_ele = page.window_height

        img1 = ft.Image(
            src=resource_path(resource_path(f"{current_working_directory}/assets/images/logo/siosk.png")),
            width=150,
            height=150,
            fit=ft.ImageFit.CONTAIN,
        )

        shadowed_img1 = ft.Container(
            img1,
            padding=5
        )

        def store_getting_lowdata(e, low_data):  # 로우 데이터 Insult를 하거나, Gettig(Polling)을 해주는 함수
            if e == 0:
                data_arrange.clear()
                data_arrange.append(low_data)
                print("\033[33m" + "LOG" + "\033[0m" + ":" + f"     Data insulting: {data_arrange}")
                return None
            elif e == 1:
                try:
                    print("\033[33m" + "LOG" + "\033[0m" + ":" + f"     Data getting: {data_arrange[0]}")
                    return data_arrange[0]
                except IndexError:
                    return None # 이부분은 개발이 완료되어지면 보안을 위해서 꼭 os._exit(0)으로 변환해주어야함.
                except Exception as e:
                    print("\033[1;91m" + "ERROR" + "\033[0m" + ":" + f"     Exception detected: {e}")
            else:
                os._exit(0)
        
        # store_getting_lowdata(1, None) 주문했던걸 반환해줌
        def build_payment_order_view():
            # if route_history[0] == "/general_order":
            future_route = "/general_order"
            # route_history.clear()

        def route_change(event: RouteChangeEvent):
            page.views.clear()
            if page.route == "/":
                page.views.append(
                    build_home_view(
                        page=page, 
                        api=self.api, 
                        shadowed_img0=shadowed_img0, 
                        shadowed_img1=shadowed_img1, 
                        width_ele=width_ele
                    )
                )
            elif page.route == "/general_order":
                page.views.append(
                    build_general_order_view(
                        page=page,
                        drinks=drinks,
                        MENU=MENU,
                        Menu=Menu,
                        key_data=key_data,
                        data_arrange=data_arrange,
                        store_getting_lowdata=store_getting_lowdata,
                        drink_items=drink_items,
                        current_working_directory=current_working_directory
                    )
                )
            elif page.route == "/siosk_order":
                page.views.append(
                    build_siosk_order_view(
                        page=page,
                        drinks=drinks,
                        MENU=MENU,
                        Menu=Menu,
                        drink_items=drink_items,
                        key_data=key_data,
                        store_getting_lowdata=store_getting_lowdata,
                        data_arrange=data_arrange,
                        current_working_directory=current_working_directory,
                        sound=self.sound
                    )
                )
            elif page.route == "/admininstrator_page":
                page.views.append(
                    administrator_page(
                        page=page,
                        data_arrange=data_arrange,
                        MENU=MENU,
                        Menu=Menu
                    )
                )
            elif page.route == "/from_general_order":
                page.views.append(
                    from_general_order(
                        page=page
                    )
                )
            elif page.route == "/from_siosk_order":
                page.views.append(
                    from_siosk_order(
                        page=page,
                        store_getting_lowdata=store_getting_lowdata,
                        data_arrange=data_arrange,
                        drink_items=drink_items,
                        resource_path=resource_path,
                        ip_store=ip_store,
                        MENU=MENU,
                        Menu=Menu
                    )
                )
            page.update()
        
        page.on_route_change = route_change
        page.go(page.route)
