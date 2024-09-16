from escpos.printer import Usb
from PIL import Image
from fastapi import FastAPI
import uvicorn

class connection:
    def __init__(self) -> None:
        self.p = Usb(0x0483, 0x5740, out_ep=0x03)

    def resize_image(self, image, max_width):
        width_percent = (max_width / float(image.size[0]))
        new_height = int((float(image.size[1]) * float(width_percent)))
        resized_image = image.resize((max_width, new_height), Image.LANCZOS)
        return resized_image

    def calculate_total_price(self, price_list: str, amounts):
        print(price_list)
        print(amounts)
        total = 0
        for i in range(len(price_list)):
            # 문자열에서 숫자 부분만 추출
            price = int(price_list[i][:-1].replace(',', '')) 
            amount = int(amounts[i])
            print(price, amount)
            total += price * amount
        print(total)
        return total

    def print(self, names, amounts, prices):
        self.p.text("                              \n")
        self.p.text("|------------SIOSK-----------|\n")
        self.p.text("|                            |\n")
        self.p.set(align='center')
        self.p.text("|                            |\n")
        self.p.text("|            Cafe24          |\n")
        self.p.text("|                            |\n")
        self.p.set(align='center')
        total_price = self.calculate_total_price(prices, amounts)

        for name, amount, price in zip(names, amounts, prices):
            self.p.text(f"|{name} X{amount}    {price}|\n")
            self.p.text(f"|                            |\n")

        self.p.text(f"|allprice:            {total_price}|\n")
        self.p.text(f"|                            |\n")
        self.p.text(f"|  kookmin:649702-01-347147  |\n")
        self.p.text(f"------------------------------\n")
        self.p.cut()

app = FastAPI()
connect = connection()

@app.get("/")
async def read_root(names: str = None, amounts: str = None, prices: str = None):
    try:
        name_list = eval(names)
        amount_list = eval(amounts)
        price_list = eval(prices)
        connect.print(name_list, amount_list, price_list)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("receipt:app", host="0.0.0.0", port=946, reload=True)