from helpers.Client import Client
import math

api = Client()

while(True):
    response = (api.get_request("/v1/s1/e1/resources/measurement")).json()

    print("Response: ", response)

    try:
        if response['distance'].endswith(" AU") or response['time'].endswith(" hours"):
            distance = float(response['distance'].split(" ")[0])
            time = float(response['time'].split(" ")[0])
        else:
            continue

    except ValueError:
        continue

    print("Distance: ", distance)
    print("Time: ", time)

    velocidade = math.trunc(distance / time)

    print("Velocidade: ", velocidade)

    response = (api.post_request("/v1/s1/e1/solution", data={
        "speed": velocidade, 
    })).json()

    print("Success!")
    print(response)

    break
