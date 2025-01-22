import asyncio
import aiohttp
import os

# Restructure the input as a list of individual items
inputs = [
    {"type": "text", "data": "a cat"},
    {"type": "text", "data": "a dog"},
    {"type": "text", "data": "Some other long text"*10},
    {"type": "image", "data": "http://images.cocodataset.org/val2017/000000039769.jpg"},
]
# multiple input to simulate many conurrent requests
inputs = inputs * 10

HF_ENDPOINT = True

if HF_ENDPOINT:
    endpoint = "https://py20wkmcjxf63zkw.us-east-1.aws.endpoints.huggingface.cloud"
    headers = {
        "Accept" : "application/json",
        "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
        "Content-Type": "application/json" 
    }
else:
    endpoint = "http://0.0.0.0:8080"
    headers = {}


async def send_request(session, input_data):
    async with session.post(endpoint + "/predict", json={"inputs": input_data}, headers=headers) as response:
        result = await response.json()
        print(f"Status: {response.status}\nResponse keys: {result.keys()}\nResponse: {result}")
        return result

async def main():
    async with aiohttp.ClientSession() as session:
        # Create tasks for all requests
        tasks = [send_request(session, input_item) for input_item in inputs]
        # Wait for all requests to complete
        results = await asyncio.gather(*tasks)
        print(f"\nAll {len(results)} requests completed!")

if __name__ == "__main__":
    asyncio.run(main())