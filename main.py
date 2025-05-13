import requests
import click

base_url = 'https://pokeapi.co/api/v2/pokemon/'
genera_url = 'https://pokeapi.co/api/v2/pokemon-species/'

def check_if_exist(response):
    if response.status_code == 200:
        return 'success'
    else:
        return 'error'

def show_data(basic_data, genera_data):
    name = str(basic_data['name'].title())
    number = int(basic_data['id'])

    if len(str(number)) == 1:
        number = '000' + str(number)
    elif len(str(number)) == 2:
        number = '00' + str(number)
    elif len(str(number)) == 3:
        number = '0' + str(number)

    height = float(basic_data['height'] / 10)
    weight = float(basic_data['weight'] / 10)

    for entry in genera_data['genera']:
        if entry["language"]["name"] == "en":
            species_title = entry["genus"]

    types = []
    for t in basic_data['types']:
        type_name = t['type']['name'].title()
        types.append(type_name)

    entries = genera_data["flavor_text_entries"]
    for entry in entries:
        if entry["language"]["name"] == "en":
            summary = entry["flavor_text"]

    stats = {}
    for stat in basic_data["stats"]:
        stat_name = stat["stat"]["name"]
        stat_value = stat["base_stat"]
        stats[stat_name] = stat_value

    rename_mapping = {
        "hp": "HP",
        "attack": "Attack",
        "defense": "Defense",
        "special-attack": "Sp. Atk",
        "special-defense": "Sp. Def",
        "speed": "Speed"
    }

    for old_key in list(stats.keys()):  # Iterate over original keys
        new_key = rename_mapping.get(old_key, old_key)  # Get new key, default to old_key if not in mapping
        stats[new_key] = stats.pop(old_key)  # Rename key

    moves = []
    for move in basic_data["moves"]:
        move_name = move["move"]["name"]
        moves.append(move_name.title())

    print(f'{name} {number}')
    print(species_title)
    print(f'{height} m / {weight} kg\n')
    print('Type: ' + ', '.join(types))
    print(f'\n{summary}\n')

    for stat, value in stats.items():
        print(f"{stat:<10} {value:>3}")

    print('\nAbility: ' + ", ".join(moves[:5]))

@click.command()
@click.argument('name')
def search_by_name(name):
    response_one = requests.get(base_url + name)
    response_two = requests.get(genera_url + name)
    if_exist_one = check_if_exist(response_one)
    if_exist_two = check_if_exist(response_two)
    if if_exist_one == 'success' and if_exist_two == 'success':
        data_one = response_one.json()
        data_two = response_two.json()
        show_data(data_one, data_two)
    else:
        print('error')

@click.command()
@click.argument('number')
def search_by_number(number):
    response_one = requests.get(base_url + number)
    response_two = requests.get(genera_url + number)
    if_exist_one = check_if_exist(response_one)
    if_exist_two = check_if_exist(response_two)
    if if_exist_one == 'success' and if_exist_two == 'success':
        data_one = response_one.json()
        data_two = response_two.json()
        show_data(data_one, data_two)
    else:
        print('error')

if __name__ == '__main__':
    search_by_name()
    search_by_number()