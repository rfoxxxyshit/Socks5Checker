
from tkinter import filedialog as fd
from tkinter import *
from tkinter import messagebox
from tkinter import Label
from tkinter import scrolledtext as ScrolledText
import logging
from tkinter import INSERT
import tkinter as tk
import aiohttp
import random
from aiohttp_socks import ProxyConnector
import asyncio
import datetime
import psutil
import os
import ssl
import time
import pytz
import json
import threading
root = Tk()
root.title('Socks5Checker GUI by rf0x3d')
root.geometry('580x100+100+200')
print("Starting")


var = IntVar()


allProxys = []
fastProxys = []
slowProxys = []
checked = []
urls = ['https://ulbwa.suicide.today/',
        'https://suicide.today/',
        'https://rf0x3d.su/',
        'https://github.com/']


class WidgetLogger(logging.Handler):
    def __init__(self, widget):
        logging.Handler.__init__(self)
        self.setLevel(logging.INFO)
        self.widget = widget
        self.widget.config(state='disabled')

    def emit(self, record):
        self.widget.config(state='normal')
        self.widget.insert(tk.END, self.format(record) + '\n')
        self.widget.see(tk.END)
        self.widget.config(state='disabled')


def fileopen():
    global file_name
    file_name = fd.askopenfilename(filetypes=(('TXT files', '*.txt'),
                                              ('All files', '*.*')))


def write():
    with open('allProxys.txt', 'w') as file:
        file.write("\n".join(allProxys))

    with open('fastProxys.txt', 'w') as file:
        file.write("\n".join(fastProxys))

    with open('slowProxys.txt', 'w') as file:
        file.write("\n".join(slowProxys))


def run():
    asyncio.run(checkProxys())


def start():
    try:
        try:
            if not file_name:
                pass
        except Exception:
            messagebox.showinfo(title='Socks5Checker GUI | WARN',
                                message='Не указан файл с proxy')
            return
        print("Получение списка прокси...")
        global proxys
        with open(file_name, 'r') as f:
            proxys = f.read().strip().split('\n')
            print('Прокси успешно загружены. Всего прокси '
                  f'загружено: {len(proxys)}.\n\n'
                  'Начинаю проверку...',
                  end=('\n\n- - - - - - - - - - - - - - - - - - -'
                       ' - - - - - - - - - - - - - - - - - \n\n'))
        msg = ("Проверка началась. За процессом можно наблюдать"
               " в окне или терминале.")
        root.geometry('580x500+100+200')
        messagebox.showinfo(title='Socks5Checker GUI | INFO', message=msg)
        thread = threading.Thread(target=run)
        thread.start()
    except Exception as e:
        root.geometry('580x500+100+200')
        logging.error(e, exc_info=True)
        print("Ошибка.")
        messagebox.showinfo(title='Socks5Checker GUI | ERROR',
                            message='При проверке прокси'
                            ' произошла ошибка. Подробнее'
                            ' в логе.')


def get_time():
    time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))

    if len(str(time.hour)) < 2:
        hour = f'0{time.hour}'
    else:
        hour = time.hour

    if len(str(time.minute)) < 2:
        minutes = f'0{time.minute}'
    else:
        minutes = time.minute

    if len(str(time.second)) < 2:
        seconds = f'0{time.second}'
    else:
        seconds = time.second

    return f'{hour}:{minutes}:{seconds}'


async def checkProxys():
    working = skipped = 0

    for proxy in proxys:
        if proxy.split(':')[0] in checked:
            skipped += 1
            continue

        url = random.choice(urls)
        logging.info('\n'
                     f'[{get_time()}] Проверяю {proxy} '
                     f'(Подключение к {url.split("/")[2]}):')
        print(f'[{get_time()}] Проверяю {proxy} '
              f'(Подключение к {url.split("/")[2]}):',
              end='\n')
        connector = ProxyConnector.from_url(f'socks5://{proxy}',
                                            limit=200,
                                            limit_per_host=200,
                                            force_close=True,
                                            enable_cleanup_closed=True,
                                            verify_ssl=False)

        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get('https://ip.beget.ru/', timeout=5) \
                        as response:
                    ip = await response.text()

                async with session.get(
                        f'http://www.geoplugin.net/json.gp?{ip}',
                        timeout=5
                ) as response:
                    country = json.loads(
                        await response.text()
                    )[
                        'geoplugin_countryName'
                    ]

                start_time_stamp = time.time()

                async with session.get(url, timeout=5):
                    await session.close()

                ping = round((time.time() - start_time_stamp) * 1000)
                allProxys.append(proxy)

                if ping <= 1100:
                    fastProxys.append(proxy)
                else:
                    slowProxys.append(proxy)

                write()

                working += 1
                checked.append(proxy.split(':')[0])
                logging.info(f'[{get_time()}] Успешное подключение! '
                             f'(Задержка: {ping} ms, IP-адрес: {ip}), '
                             f'страна: {country})\n',
                             )
                print(f'[{get_time()}] Успешное подключение! '
                      f'(Задержка: {ping} ms, IP-адрес: {ip}), '
                      f'страна: {country})',
                      end=('\n\n- - - - - - - - - - - - - - - - - - - - - - '
                           '- - - - - - - - - - - - - - \n\n'))
        except Exception:
            skipped += 1
            checked.append(proxy.split(':')[0])
            logging.info(f'[{get_time()}] Неудачное подключение.')
            print(f'[{get_time()}] Неудачное подключение.',
                  end=('\n\n- - - - - - - - - - - - - - - - '
                       '- - - - - - - - - - '
                       '- - - - - - - - - - \n\n'))

    message = (f'Проверка завершена! Нашлись {working} работоспособных прокси.'
               f' {skipped} прокси были пропущены.\n'
               f'Все работоспособные прокси сохранены в файле allProxys.txt.\n'
               'Быстрые прокси сохранены в файле fastProxys.txt\n'
               'Медленные прокси сохранены в файле slowProxys.txt')

    print(message,
          end=('\n\n- - - - - - - - - - - - - - - - '
               '- - - - - - - - - - '
               '- - - - - - - - - - \n\n'))
    logger.info("Проверка завершена.")
    messagebox.showinfo(title='Socks5Checker GUI | INFO', message=message)
    proxys.clear()
    allProxys.clear()
    fastProxys.clear()
    slowProxys.clear()
    checked.clear()


root.resizable(False, False)
file = Button(text='Выбрать файл с proxy', command=fileopen)
file.place(x=580/2-70, y=15)
crack = Button(text='Старт', height=2, width=12, background='green',
               command=start)
crack.pack()
crack.place(x=580/2-50, y=55)
st = ScrolledText.ScrolledText(root, state='disabled')
st.configure(font='TkFixedFont', fg="#fff")
st.grid(column=0, row=1, sticky='w', columnspan=4)
st.pack()
st.place(x=0, y=110)
loggers = WidgetLogger(st)
logging.basicConfig(filename='app.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.addHandler(loggers)
logger.info("Socks5Checker GUI Initialized")
print("Started!")
root.mainloop()
