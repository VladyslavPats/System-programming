import asyncio
import random

# Асинхронна функція, яка імітує виконання задачі
async def do_task(task_id):
    delay = random.uniform(0.1, 3.0)
    await asyncio.sleep(delay)
    print(f"Задача {task_id} завершилась за {delay:.2f} секунд")

# Основна функція
async def main():
    tasks = [do_task(i) for i in range(1, 6)]  # створюємо 5 задач

    try:
        # Обмежуємо загальний час виконання до 2 секунд
        await asyncio.wait_for(asyncio.gather(*tasks), timeout=2.0)
    except asyncio.TimeoutError:
        print("\n⏰ Час виконання перевищено! Деякі задачі не завершилися вчасно.")

# Запуск програми
if __name__ == "__main__":
    asyncio.run(main())
