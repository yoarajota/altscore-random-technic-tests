from helpers.Client import Client
import math

api = Client()

count_stars = 0
max_pages = None
page = 1
count_resonance = 0

while(True):
    response = api.get_request("/v1/s1/e2/resources/stars",
        params={
            "page": page,
            "sort-by": "resonance",
            "sort-direction": "desc"
        }
    )

    headers = response.headers
    json = response.json()

    stars = len(json)

    if max_pages is None:
        x_total_count = int(headers['x-total-count'])

        module = x_total_count % stars

        max_pages = int(x_total_count / stars) + module

    count_stars += stars

    for star in json:
        count_resonance += star['resonance']

    print("Stars: ", stars)	
    print("count_resonance: ", count_resonance)
    
    if page == max_pages:
        break

    page += 1

response = (api.post_request("/v1/s1/e2/solution", data={
    "average_resonance": math.trunc(count_resonance / count_stars),
})).json()

print("Success!")
print(response)