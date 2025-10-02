from typing import MutableMapping, Any, Callable, Awaitable

# Визначаємо типи для ASGI - це словники з різними типами даних
Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]
Receive = Callable[[], Awaitable[Message]]  # Функція, яка асинхронно отримує повідомлення
Send = Callable[[Message], Awaitable[None]]  # Функція, яка асинхронно відправляє повідомлення

total_connections = 0  # Лічильник підключень до сервера

# Функція для обробки lifespan протоколу (запуск і завершення сервера)
async def handle_lifespan(scope: Scope, receive: Receive, send: Send) -> None:
    while True:
        message = await receive()  # Чекаємо на повідомлення від сервера
        print(f"lifespan message received: {message}")

        if message["type"] == "lifespan.startup":
            print("Server is starting up...")  # Повідомляємо про старт сервера
            await send({"type": "lifespan.startup.complete"})  # Відповідаємо серверу, що старт пройшов успішно
        elif message["type"] == "lifespan.shutdown":
            print("Server is shutting down...")  # Повідомляємо про вимкнення сервера
            await send({"type": "lifespan.shutdown.complete"})  # Відповідаємо серверу, що вимкнення завершено
            break  # Виходимо з циклу, бо сервер вимикається

# Функція, що повертає відповідь для GET /hello
async def hello_endpoint(scope: Scope, receive: Receive, send: Send) -> None:
    # Відправляємо HTTP заголовки і статус 200 OK
    response_start = {
        "type": "http.response.start",
        "status": 200,
        "headers": [
            [b"content-type", b"text/plain"],  # Заголовок content-type має бути байтовим рядком
        ],
    }
    await send(response_start)

    # Відправляємо тіло відповіді
    response_body = {
        "type": "http.response.body",
        "body": b"Hello, world!",  # Тіло теж байти
        "more_body": False,  # Показуємо, що більше частин відповіді немає
    }
    await send(response_body)

# Функція, що повертає відповідь для GET /goodbye
async def goodbye_endpoint(scope: Scope, receive: Receive, send: Send) -> None:
    response_start = {
        "type": "http.response.start",
        "status": 200,
        "headers": [
            [b"content-type", b"text/plain"],
        ],
    }
    await send(response_start)

    response_body = {
        "type": "http.response.body",
        "body": b"Goodbye, world...",  # Тіло відповіді
        "more_body": False,
    }
    await send(response_body)

# Основна функція для обробки HTTP-запитів
async def handle_http(scope: Scope, receive: Receive, send: Send) -> None:
    while True:
        message = await receive()  # Отримуємо повідомлення від клієнта (браузера, curl тощо)
        print(f"http message received: {message}")

        # Якщо клієнт відключився — закриваємо цикл і припиняємо обробку
        if message["type"] == "http.disconnect":
            print("Client disconnected")
            break

        # Якщо отримали HTTP запит — обробляємо його
        elif message["type"] == "http.request":
            path = scope.get("path", "")  # Витягуємо шлях запиту
            method = scope.get("method", "")  # Витягуємо HTTP метод (GET, POST тощо)

            # Прості роутинг умови
            if path == "/hello" and method == "GET":
                await hello_endpoint(scope, receive, send)
            elif path == "/goodbye" and method == "GET":
                await goodbye_endpoint(scope, receive, send)
            else:
                # Якщо шлях невідомий — повертаємо 404 Not Found
                response_start = {
                    "type": "http.response.start",
                    "status": 404,
                    "headers": [
                        [b"content-type", b"text/plain"],
                    ],
                }
                await send(response_start)

                response_body = {
                    "type": "http.response.body",
                    "body": b"Not Found",
                    "more_body": False,
                }
                await send(response_body)
            break  # Після відповіді виходимо з циклу

# Головна функція ASGI-додатку
async def app(scope: Scope, receive: Receive, send: Send) -> None:
    global total_connections
    total_connections += 1
    current_connection = total_connections
    print(f"Connection {current_connection}: Scope: {scope}")  # Виводимо інформацію про підключення

    # Визначаємо тип запиту і виконуємо відповідну обробку
    if scope["type"] == "lifespan":
        await handle_lifespan(scope, receive, send)
    elif scope["type"] == "http":
        await handle_http(scope, receive, send)

    print(f"Connection {current_connection}: Completed")  # Виводимо повідомлення про завершення обробки

# Функція для запуску сервера через uvicorn
def main():
    import uvicorn

    uvicorn.run(
        app,
        port=5000,           # Порт, на якому запускаємо сервер
        log_level="info",    # Рівень логів
        use_colors=False,    # Вимкнути кольорові логи (зручно для деяких терміналів)
    )

# Якщо цей файл запускається напряму — запускаємо сервер
if __name__ == "__main__":
    main()
