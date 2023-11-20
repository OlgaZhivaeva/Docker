import asyncio

import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
        # async with session.post('http://127.0.0.1:8080/advertisements',
        #                          json = {'heading': 'Школа танцев',
        #                                 'description': 'Набор девочек и мальчиков. Возраст 7-12 лет',
        #                                 'creator': 'Школа бальных танцев Арт-студия'},) as response:
        #     print(response.status)
        #     print(await response.json())

        async with session.post('http://127.0.0.1:8080/advertisements',
                                json = {'id': 1,
                                       'heading': 'Щенки ВЕО',
                                       'description': 'Щенки ВЕО от титулованных родителей',
                                       'creator': 'Питомник ВЕО'},) as response:
           print(response.status)
           print(await response.json())

        async with session.get('http://127.0.0.1:8080/advertisements/1',) as response:
            print(response.status)
            print(await response.json())

        # async with session.get('http://127.0.0.1:8080/users/100',) as response:
        #     print(response.status)
        #     print(await response.json())

        # async with session.patch('http://127.0.0.1:8080/advertisements/1',
        #                         json={'heading': 'Школа бальных танцев'},) as response:
        #     print(response.status)
        #     print(await response.json())
        #
        # async with session.get('http://127.0.0.1:8080/advertisements/1',) as response:
        #     print(response.status)
        #     print(await response.json())

        # async with session.delete("http://127.0.0.1:8080/advertisements/2",) as response:
        #     print(response.status)
        #     print(await response.json())
        #
        # async with session.get("http://127.0.0.1:8080/advertisements/2",) as response:
        #     print(response.status)
        #     print(await response.json())


asyncio.run(main())