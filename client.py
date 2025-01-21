import requests

texts = ["a cat", "a dog", "a bird"]
image_urls = ["http://images.cocodataset.org/val2017/000000039769.jpg", "http://images.cocodataset.org/val2017/000000039769.jpg"]

response = requests.post("http://0.0.0.0:8080/predict", json={"image_urls": image_urls, "texts": texts})
print(f"Status: {response.status_code}\nResponse:\n {response.text}")
