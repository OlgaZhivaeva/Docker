import requests
import datetime

def get_value_from_link(url):
    response = requests.get(url).json()
    return response

def transform(json, key, name):
    """Преобразование списка ссылок в строку с названиями через запятую"""

    list_url = json[key]
    list_title = [get_value_from_link(url)[name] for url in list_url]
    json[key] = ', '.join(list_title)
    return json



def main():
    for person_id in range(1, 6):
        person = get_value_from_link(f'https://swapi.dev/api/people/{person_id}/')
        transform(person, 'films', 'title')
        transform(person, 'species', 'name')
        transform(person, 'vehicles', 'name')
        transform(person, 'starships', 'name')

        print(person)



if __name__ == '__main__':
    start = datetime.datetime.now()
    main()
    print(datetime.datetime.now() - start)
