import asyncio
import random
import time

# Асинхронна функція, що імітує роботу
async def do_work(task_id):
    delay = random.randint(1, 3)
    await asyncio.sleep(delay)
    print(f"Завдання {task_id} завершено за {delay} секунд")

# Послідовне виконання
async def run_sequential():
    print("\nПослідовне виконання:")
    start = time.time()
    for i in range(1, 6):
        await do_work(i)
    end = time.time()
    print(f"Час виконання (послідовно): {end - start:.2f} секунд")

# Конкурентне виконання
async def run_concurrent():
    print("\nКонкурентне виконання:")
    start = time.time()
    tasks = [do_work(i) for i in range(1, 6)]
    await asyncio.gather(*tasks)
    end = time.time()
    print(f"Час виконання (одночасно): {end - start:.2f} секунд")

# Основна функція
async def main():
    await run_sequential()
    await run_concurrent()

# Запуск
if __name__ == "__main__":
    asyncio.run(main())
