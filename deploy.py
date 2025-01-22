from huggingface_hub import create_inference_endpoint
import os
from dotenv import load_dotenv
import re


IMAGE_URL = "moritzlaurer/litserve-huggingface-ie-siglip:0.0.8-siglip-so400m-patch14-384"
MODEL_ID = "google/siglip-so400m-patch14-384"  #"google/siglip-base-patch16-224"
ENDPOINT_NAME = "siglip-so400m-patch14-384-litserve-011"

def create_compatible_endpoint_name(model_id: str) -> str:
    part = model_id.split('/')[-1]
    part_lower = part.lower()
    cleaned = re.sub(r'[^a-z0-9\-]', '-', part_lower)
    trimmed = cleaned[:32]
    return trimmed


if __name__ == "__main__":
    load_dotenv()
    repo_id = MODEL_ID
    env_vars = {}

    endpoint = create_inference_endpoint(
        name=ENDPOINT_NAME,  #create_compatible_endpoint_name(MODEL_ID),
        repository=repo_id,
        framework="pytorch",
        task="custom",
        accelerator="gpu",
        vendor="aws",
        region="us-east-1",
        type="protected",
        instance_size="x1",
        instance_type="nvidia-a10g",
        min_replica=0,
        max_replica=1,
        scale_to_zero_timeout=30,
        custom_image={
            "health_route": "/health",
            "env": env_vars,
            "url": IMAGE_URL,
            "port": 8080,
        },
        token=os.getenv("HF_TOKEN"),
    )
    
    print(f"Go to https://ui.endpoints.huggingface.co/{endpoint.namespace}/endpoints/{endpoint.name} to see the endpoint status.")
