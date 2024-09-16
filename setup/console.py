import curses
from Siosk_en.package.model import API
from Siosk_en.package.scan import find_process_by_port
from auto.delete import delete_dot_underscore_files
from curses import wrapper
from auto.clear_terminal import clear_terminal
import os
import time
import warnings

warnings.simplefilter("ignore")

class TerminalUI:
    def __init__(self) -> None:
        bool_data = find_process_by_port(9460) # Check 9460 Port 
        if bool_data == True:
            self.api = API(
                token="SioskKioskFixedTokenVerifyingTokenData", # Is Python is running, Process in Local
                url="http://127.0.0.1"
            )
        elif bool_data == False:
            self.api = API(
                token="SioskKioskFixedTokenVerifyingTokenData", # If None run as Server
                url="https://anoask.site"
            )
        self.api.access_server()
        time.sleep(3)
        os.system(clear_terminal())

    def main(self, stdscr):
        curses.curs_set(1)
        stdscr.clear()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) 
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

        chat_height = curses.LINES - 3
        input_height = 3
        chat_win = curses.newwin(chat_height, curses.COLS, 0, 0)
        input_win = curses.newwin(input_height, curses.COLS, chat_height, 0)
        input_win.border()
        chat_win.scrollok(True)
        chat_win.refresh()
        input_win.refresh()

        messages = []
        max_messages = chat_height - 1

        while True:
            input_win.clear()
            input_win.border()
            input_win.addstr(1, 1, "You: ", curses.color_pair(1) | curses.A_BOLD)
            input_win.refresh()

            curses.echo()
            user_input = input_win.getstr(1, 7, curses.COLS - 9).decode('utf-8', 'replace')
            curses.noecho()
            if user_input.lower() == 'exit':
                break

            messages.append(f"You: {user_input}")
            chat_win.clear()

            start_idx = max(0, len(messages) - chat_height + 1)
            for idx, message in enumerate(messages[start_idx:]):
                try:
                    if message.startswith("You: "):
                        chat_win.addstr(idx, 1, message, curses.color_pair(1) | curses.A_BOLD)
                    elif message.startswith("AI: "):
                        chat_win.addstr(idx, 1, message, curses.color_pair(2) | curses.A_BOLD)
                    else:
                        chat_win.addstr(idx, 1, message, curses.color_pair(2))
                except curses.error as e:
                    pass
            chat_win.refresh()

            self.api.texture_preparing() # Loading variable token, url to process targeting to class
            Q, A, F, embedding_time = self.api.texture(user_input) # call fuction that send get signal to Server
            ai_response = f"AI: {A}"
            messages.append(ai_response)

            chat_win.clear()
            start_idx = max(0, len(messages) - chat_height + 1)
            for idx, message in enumerate(messages[start_idx:]):
                try:
                    if str(message).startswith("You: "):
                        chat_win.addstr(idx, 1, message, curses.color_pair(1) | curses.A_BOLD)
                    elif str(message).startswith("AI: "):
                        chat_win.addstr(idx, 1, message, curses.color_pair(2) | curses.A_BOLD)
                    else:
                        chat_win.addstr(idx, 1, message, curses.color_pair(2))
                except curses.error as e:
                    os._exit(0)
            chat_win.refresh()
            if A == "카드를 삽입해주십시오. 결제가 완료되었습니다 방문해주셔서 감사합니다":
                os._exit(0)
        curses.endwin()

if __name__ == "__main__":
    delete_dot_underscore_files()
    Terminal = TerminalUI()
    wrapper(Terminal.main)