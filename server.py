import litserve as ls
from transformers import AutoModel, AutoProcessor
from PIL import Image
import requests

class SimpleLitAPI(ls.LitAPI):
    def setup(self, device):
        self.device = device
        self.model = AutoModel.from_pretrained("google/siglip-base-patch16-224").to(device)
        self.processor = AutoProcessor.from_pretrained("google/siglip-base-patch16-224")

    def decode_request(self, request):
        print(request)
        result = {}
        if "texts" in request:
            result["texts"] = request["texts"]
        if "image_urls" in request:
            result["image_urls"] = request["image_urls"]
        return result

    def predict(self, inputs):
        print(inputs)
        
        if "texts" in inputs:
            texts = inputs["texts"]
            text_inputs = self.processor(text=texts, padding="max_length", return_tensors="pt")
            text_inputs = {k: v.to(self.device) for k, v in text_inputs.items()}
            text_outputs = self.model.text_model(text_inputs["input_ids"])
        else:
            text_outputs = None
        
        if "image_urls" in inputs:
            images = [Image.open(requests.get(image_url, stream=True).raw) for image_url in inputs["image_urls"]]
            image_inputs = self.processor(images=images, padding="max_length", return_tensors="pt")
            image_inputs = {k: v.to(self.device) for k, v in image_inputs.items()}
            image_outputs = self.model.vision_model(image_inputs["pixel_values"])
        else:
            image_outputs = None

        return {
            "text_outputs": text_outputs, 
            "image_outputs": image_outputs
        }

    def encode_response(self, output):
        return {
            "text_embeds": output["text_outputs"].pooler_output.detach().cpu().numpy().tolist() if output["text_outputs"] is not None else None, 
            "image_embeds": output["image_outputs"].pooler_output.detach().cpu().numpy().tolist() if output["image_outputs"] is not None else None
        }

if __name__ == "__main__":
    api = SimpleLitAPI()
    server = ls.LitServer(api, accelerator="auto", track_requests=True)
    server.run(port=8080)
