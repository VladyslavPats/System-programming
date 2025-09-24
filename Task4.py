import aiohttp
import asyncio
import os
import time
import random

# Створення папки для зображень, якщо не існує
os.makedirs("images", exist_ok=True)

# Функція для запису зображення у файл
def write_image(data):
    timestamp = int(time.time() * 1000)  # унікальна мітка часу в мс
    filename = f"images/image_{timestamp}.jpg"
    with open(filename, "wb") as f:
        f.write(data)

# Асинхронне завантаження одного зображення
async def fetch_content(url, session):
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.read()
            write_image(data)
        else:
            print(f"⚠️ Не вдалося завантажити: {url} | Статус: {response.status}")

# Генерація списку URL (Picsum – можна використовувати такі посилання)
def generate_image_urls(count):
    return [f"https://picsum.photos/200/300?random={random.randint(1, 10000)}" for _ in range(count)]

# Послідовне завантаження
async def sequential_download(urls):
    async with aiohttp.ClientSession() as session:
        for url in urls:
            await fetch_content(url, session)

# Конкурентне завантаження
async def concurrent_download(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_content(url, session) for url in urls]
        await asyncio.gather(*tasks)

# Основна функція
async def main():
    count = 20  # Кількість зображень (можеш змінити на 10–50)
    urls = generate_image_urls(count)

    print(f"\n📥 Послідовне завантаження {count} зображень...")
    start_seq = time.time()
    await sequential_download(urls)
    end_seq = time.time()
    print(f"⏱️ Час послідовного завантаження: {end_seq - start_seq:.2f} секунд")

    print(f"\n📥 Конкурентне завантаження {count} зображень...")
    start_conc = time.time()
    await concurrent_download(urls)
    end_conc = time.time()
    print(f"⏱️ Час конкурентного завантаження: {end_conc - start_conc:.2f} секунд")

# Запуск
if __name__ == "__main__":
    asyncio.run(main())
