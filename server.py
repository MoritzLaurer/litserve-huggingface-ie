import litserve as ls
from transformers import AutoModel, AutoProcessor
from PIL import Image
import requests
from pydantic import BaseModel
from typing import Literal

# optional: for request input validation
class Input(BaseModel):
    type: Literal["text", "image"]
    data: str

class PredictRequest(BaseModel):
    inputs: Input

class SimpleLitAPI(ls.LitAPI):
    def setup(self, device):
        self.device = device
        self.model = AutoModel.from_pretrained("google/siglip-so400m-patch14-384").to(device)  # google/siglip-base-patch16-224
        self.processor = AutoProcessor.from_pretrained("google/siglip-so400m-patch14-384")

    def decode_request(self, request: PredictRequest):
        print("request:\n", request)
        return request.inputs

    def predict(self, inputs):
        print("inputs:\n", inputs)  
        # server receives the inputs as a batch/list of dicts
        # need to separate texts from images, because siglip processes them differently     
        texts = [item.data for item in inputs if item.type == "text"]
        image_urls = [item.data for item in inputs if item.type == "image"]
        
        if texts:
            text_inputs = self.processor(text=texts, padding="max_length", return_tensors="pt")
            text_inputs = {k: v.to(self.device) for k, v in text_inputs.items()}
            text_outputs = self.model.text_model(text_inputs["input_ids"])
        
        if image_urls:
            images = [Image.open(requests.get(url, stream=True).raw) for url in image_urls]
            image_inputs = self.processor(images=images, padding="max_length", return_tensors="pt")
            image_inputs = {k: v.to(self.device) for k, v in image_inputs.items()}
            image_outputs = self.model.vision_model(image_inputs["pixel_values"])

        # Return embeddings in the same order as inputs
        results = []
        text_idx = 0
        image_idx = 0
        
        for item in inputs:
            if item.type == "text":
                embed = text_outputs.pooler_output[text_idx].detach().cpu().numpy().tolist()
                results.append({"type": "text", "embedding": embed})
                text_idx += 1
            elif item.type == "image":
                embed = image_outputs.pooler_output[image_idx].detach().cpu().numpy().tolist()
                results.append({"type": "image", "embedding": embed})
                image_idx += 1
            else:  # this should never happen given the input validation above
                raise ValueError(f"Invalid input type: {item.type}")
                
        return results

    def encode_response(self, output):
        return output

if __name__ == "__main__":
    api = SimpleLitAPI()
    server = ls.LitServer(api, accelerator="auto", max_batch_size=32, batch_timeout=0.05, track_requests=True, timeout=30)
    server.run(port=8080)
