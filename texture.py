from Siosk.package.model import API
from auto.delete import delete_dot_underscore_files
import os

current_working_directory = os.getcwd()
api = API(token="SioskKioskFixedTokenVerifyingTokenData")

def ask_res():
    while True:
        data = input("Q: ")
        api.texture_preparing()
        result, embedding_time = api.texture(data)
        print("A: " + result)
        print("T: " + str(embedding_time))

if __name__ == "__main__":
    delete_dot_underscore_files()
    ask_res()