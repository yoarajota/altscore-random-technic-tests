from helpers.Client import Client
import math
import base64

api = Client()


# while(True):
#     response = (api.post_request("/v1/s1/e8/actions/door"))

#     print("Response: ", response)
#     print("Status Code: ", response.status_code)
#     print("Headers: ", response.headers)
#     print("Content: ", response.content)

#     print("Response: ", response.json())

# second tip
cookie = "QWx0d2FydHM="

# response = (api.post_request("/v1/s1/e8/actions/door", cookies={"gryffindor": cookie}))

# print("Response: ", response)
# print("Status Code: ", response.status_code)
# print("Headers: ", response.headers)
# print("Content: ", response.content)

# print(response.json())

# third tip

# fixing typo

# other coockie
# cookie = "c3VyZ2U="

# loop cookies until the end

concat = base64.b64decode(cookie).decode("utf-8")

while(True):
    response = (api.post_request("/v1/s1/e8/actions/door", cookies={"gryffindor": cookie}))

    # get set-cookie from response
    cookie = response.cookies.get("gryffindor")

    if cookie is None:
        break

    concat += " " + base64.b64decode(cookie).decode("utf-8")

    print(response.headers)
    print("Response: ", response.json())

print(concat)

# ultimo cookie = Y29udGludWFtZW50ZQ==
# cookie = "Y29udGludWFtZW50ZQ=="

# response = (api.post_request("/v1/s1/e8/actions/door", data={
#     "hidden_message": "revelio",
# }, cookies={"gryffindor": cookie, "conjuro": "revelio", "conjuro2": "revelio", "spell": "revelio"}))	

# print("Response: ", response)
# print("Status Code: ", response.status_code)
# print("Headers: ", response.headers)
# print("Content: ", response.content)
# print(response.json())