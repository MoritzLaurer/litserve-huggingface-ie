import requests

# Restructure the input as a list of individual items
inputs = [
    {"type": "text", "data": "a cat"},
    {"type": "text", "data": "a dog"},
    {"type": "image", "data": "http://images.cocodataset.org/val2017/000000039769.jpg"},
    {"type": "image", "data": "http://images.cocodataset.org/val2017/000000039769.jpg"}
]

for input in inputs:
    response = requests.post("http://0.0.0.0:8080/predict", json={"inputs": input})
    print(f"Status: {response.status_code}\nResponse keys:\n {response.json().keys()}")

#print(responses)
