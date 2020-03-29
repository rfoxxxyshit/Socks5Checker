import aiohttp
import random
from aiohttp_socks import ProxyConnector
import asyncio
import datetime
import psutil
import os


def clearConsole():
    if psutil.WINDOWS:
        return os.system("cls")
    else:
        return os.system("clear")


urls = ['https://ulbwa.suicide.today/',
        'https://spotify.com/',
        'https://github.com/Ulbwaa',
        'https://www.youtube.com/',
        'https://www.minecraft.net/',
        'https://mail.ru/',
        'https://pypi.org/',
        'https://yandex.ru/',
        'https://www.deezer.com/',
        'https://play.google.com/',
        'https://suicide.today/']

allProxys = []
fastProxys = []
slowProxys = []
checked = []

clearConsole()

try:
    with open('proxy.txt', 'r') as f:
        proxys = f.read().split('\n')
        print(f'Прокси успешно загружены. Всего прокси загружено: {len(proxys)}. '
              f'Начинаю проверку...')
except FileNotFoundError:
    print('Файл proxy.txt не найден. Пожалуйста, создайте его и поместите '
          'туда список ваших прокси для обеспечения работоспособности скрипта.')
    exit(-1)


def write():
    with open('allProxys.txt', 'w') as file:
        file.write("\n".join(allProxys))

    with open('fastProxys.txt', 'w') as file:
        file.write("\n".join(fastProxys))

    with open('slowProxys.txt', 'w') as file:
        file.write("\n".join(slowProxys))


async def checkProxys():
    i = 0
    r = 0

    for proxy in proxys:
        if proxy.split(':')[0] in checked:
            r += 1
            continue

        url = random.choice(urls)
        print(f'Проверяю {proxy} (Подключение к {url.split("/")[2]}):', end=' ')
        connector = ProxyConnector.from_url(f'socks5://{proxy}')

        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                start_time_stamp = datetime.datetime.timestamp(datetime.datetime.now())
                async with session.get(url, timeout=5):
                    ping = datetime.datetime.timestamp(datetime.datetime.now()) - start_time_stamp
                    allProxys.append(proxy)

                    if ping <= 1:
                        fastProxys.append(proxy)
                    else:
                        slowProxys.append(proxy)

                    write()

                    i += 1
                    checked.append(proxy.split(':')[0])
                    print(f'Успешное подключение! (Задержка: {ping} секунд)', end='\n')
        except (Exception, BaseException):
            r += 1
            checked.append(proxy.split(':')[0])
            print(f'Неудачное подключение.', end='\n')

    print(f'\n\n\nПроверка завершена! Нашлись {i} работоспособных прокси. {r} прокси были пропущены.\n'
          f'Все работоспособные прокси сохранены в файле allProxys.txt.\n'
          'Быстрые прокси сохранены в файле fastProxys.txt\n'
          'Медленные прокси сохранены в файле slowProxys.txt')


try:
    asyncio.run(checkProxys())
except RuntimeError:
    exit(0)
