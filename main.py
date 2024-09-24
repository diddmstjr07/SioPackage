import flet as ft
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from SioskUI.siosk import UI
from Siosk.package.exit_manager import EXITING

if __name__ == "__main__":
    try:
        ui = UI()
        ft.app(target=ui.main)
    except KeyboardInterrupt:
        EXITING()