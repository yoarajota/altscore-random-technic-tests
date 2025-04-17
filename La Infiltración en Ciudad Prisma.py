import requests
import statistics
import concurrent.futures
from helpers.Client import Client

api = Client()

def get_all_types():
    response = requests.get("https://pokeapi.co/api/v2/type")
    data = response.json()
    types = [t for t in data["results"] if t["name"] not in ["unknown", "shadow"]]
    
    return sorted(types, key=lambda x: x["name"])

def get_pokemon_by_type(type_url):
    response = requests.get(type_url)
    data = response.json()
    return data["pokemon"]

def get_pokemon_height(pokemon_entry):
    pokemon_url = pokemon_entry["pokemon"]["url"]

    try:
        response = requests.get(pokemon_url)
        data = response.json()

        return data["height"]
    except Exception as e:
        return None

def process_type(type_info):
    type_name = type_info["name"]
    print(f"Processando tipo: {type_name}")
    
    pokemon_list = get_pokemon_by_type(type_info["url"])
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        heights = list(filter(None, executor.map(get_pokemon_height, pokemon_list)))
    
    if heights:
        avg_height = statistics.mean(heights)
        return (type_name, avg_height)
    return None

types = get_all_types()

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(filter(None, executor.map(process_type, types)))

heights_dict = {type_name: avg_height for type_name, avg_height in results}

print(heights_dict)

result = (api.post_request("/v1/s1/e6/solution", data={
    "heights": heights_dict,
})).json()

print(f"Resultado: {result}")