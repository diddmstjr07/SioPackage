from escpos.printer import Usb
from PIL import Image

class connection:
    def __init__(self) -> None:
        self.p = Usb(0x0483, 0x5740, out_ep=0x03)

    def resize_image(self, image, max_width):
        width_percent = (max_width / float(image.size[0]))
        new_height = int((float(image.size[1]) * float(width_percent)))
        resized_image = image.resize((max_width, new_height), Image.LANCZOS)
        return resized_image

    def calculate_total_price(self, price_list, amounts):
        total_price = 0
        for price, amount in zip(price_list, amounts):
            price_num = int(''.join(filter(str.isdigit, price)))
            total_price += price_num * int(amount)  # amount를 정수로 변환하여 계산
        return f"{total_price:,}원"  # 쉼표 추가 및 '원' 붙이기

    def print(self, names, amounts, prices):
        self.p.set(align='center')
        self.p.text(f"                              \n")
        total_price = self.calculate_total_price(prices, amounts)

        for name, amount, price in zip(names, amounts, prices):
            self.p.text(f"|{name} X{amount}    {price}|\n")
            self.p.text(f"|                            |\n")

        self.p.text(f"|allprice:            {total_price}|\n")
        self.p.text(f"|                            |\n")
        self.p.text(f"|  kookmin:649702-01-347147  |\n")
        self.p.text(f"------------------------------\n")
        self.p.cut()
