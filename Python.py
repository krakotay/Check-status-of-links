import aiohttp
import polars as pl
import os
import asyncio

data = pl.read_excel('Ссылки для проверки.xlsx').unique().filter((pl.col("Ссылка") != ''))
print(data)
global i
i = 0
async def check(link):    
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            if response.status == 404:
                return '404'
            else:
                return 'Ссылка работает'
                i += 1


async def main(data):
    # Создаем список задач для асинхронного выполнения
    tasks = [check(link) for link in data['Ссылка']]
    # Запускаем задачи и ожидаем результатов
    results = await asyncio.gather(*tasks)

    # Обновляем данные в поларсе с результатами проверки
    data = data.with_columns(Проверка=pl.Series(results))

    # Выводим результаты на экран
    print(data)
    data.write_excel('result.xlsx')
    print(i)
    os.system('pause')
    

if __name__ == "__main__":
    asyncio.run(main(data))
