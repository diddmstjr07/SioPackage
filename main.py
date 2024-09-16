import flet as ft
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from SioskUI.siosk import UI

if __name__ == "__main__":
    ui = UI()
    ft.app(target=ui.main)