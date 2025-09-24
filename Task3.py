import asyncio
import random

# Асинхронна задача з використанням семафора
async def limited_task(task_id, semaphore):
    async with semaphore:
        print(f"🔄 Задача {task_id} почалась")
        delay = random.uniform(0.1, 1.0)
        await asyncio.sleep(delay)
        print(f"✅ Задача {task_id} завершилась за {delay:.2f} секунд")

# Основна функція
async def main():
    semaphore = asyncio.Semaphore(5)  # обмеження на 5 одночасних задач
    tasks = [limited_task(i, semaphore) for i in range(1, 51)]  # 50 задач
    await asyncio.gather(*tasks)

# Запуск програми
if __name__ == "__main__":
    asyncio.run(main())
