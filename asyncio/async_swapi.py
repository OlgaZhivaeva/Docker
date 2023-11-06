import asyncio
import aiohttp
import datetime

from more_itertools import chunked

from models import init_db, People, Session

CHUNK_SIZE = 10

async def paste_to_db(people):
    async with Session() as session:
        for person in people:
            people = People(
                            birth_year=person.get('birth_year'),
                            eye_color=person.get('eye_color'),
                            films=person.get('films'),
                            hair_color=person.get('hair_color'),
                            height=person.get('height'),
                            homeworld=person.get('homeworld'),
                            mass=person.get('mass'),
                            name=person.get('name'),
                            skin_color=person.get('skin_color'),
                            species=person.get('species'),
                            starships=person.get('starships'),
                            vehicles=person.get('vehicles')
                            )
            session.add(people)
        await session.commit()

async def get_person(person_id, session):
    person = await get_value_from_link(f'https://swapi.py4e.com/api/people/{person_id}/', session)
    person = await transform(person, 'films', 'title', session)
    person = await transform(person, 'species', 'name', session)
    person = await transform(person, 'vehicles', 'name', session)
    person = await transform(person, 'starships', 'name', session)
    return person

async def get_value_from_link(url, session):
    response = await session.get(url)
    json = await response.json()
    return json

async def transform(json, key, name, session):
    """Преобразование списка ссылок в строку с названиями через запятую"""

    if json != None:
        list_url = json.get(key)
        if list_url != None:
            coros = [get_value_from_link(url, session) for url in list_url]
            result = await asyncio.gather(*coros)
            list_title = [res[name] for res in result]
            json[key] = ', '.join(list_title)
    return json


async def main():
    await init_db()

    async with aiohttp.ClientSession() as session:

        for people_id_chunk in chunked(range(1, 100), CHUNK_SIZE):
            coros = [get_person(people_id, session) for people_id in people_id_chunk]
            result = await asyncio.gather(*coros)
            asyncio.create_task(paste_to_db(result))

    tasks_to_await = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks_to_await)

start = datetime.datetime.now()
asyncio.run(main())
print(datetime.datetime.now() - start)
