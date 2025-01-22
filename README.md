
# Deploying LitServe containers on Hugging Face Dedicated Endpoints

[LitServe](https://lightning.ai/docs/litserve/home) is a flexible AI model serving engine.

[Hugging Face Dedicated Endpoints](https://huggingface.co/docs/inference-endpoints/index) is a platform for hosting and serving AI models.

This repository provides guidance for how to build a custom LitServe container and deploy it on Hugging Face Dedicated Endpoints.


## Setup

1. Clone this repository.

2. Create a virtual environment and install the dependencies (this repo uses `poetry`). This should work with something like `poetry install`.

3. Create a `server.py` file following the [LitServe docs](https://lightning.ai/docs/litserve/home/get-started). This repo contains an example `server.py` file, illustrating how to create a multimodal embedding server with the SigLIP model for both image and text embeddings with batched processing.

4. Test the server locally. Run `python server.py` in the terminal to start the server. Then you can make requests to the server. The example `client.py` file illustrates how to make requests to the SigLIP server (run via `python client.py`). `client_async.py` illustrates how to make requests to the server asynchronously to simulate several concurrent user requests.

5. If the server works locally, you can build the container and push it to Docker Hub. The `Dockerfile` determines how the container will be built. This file is designed for endpoints that should run on Nvidia GPUs. The LitServe [Dockerization docs](https://lightning.ai/docs/litserve/features/dockerization-deployment) provide guidance for dockerizing your server.
   - The container will build its dependencies from the requirements.txt file. In case your `server.py` file requires additional dependencies, update the `requirements.txt` file accordingly.
   - The `endpoints-entrypoint.sh` is required for the container to run on Hugging Face Endpoints and you can keep it as-is.
   - You then need to build the container and push it to Docker Hub. This is implemented in the `build_push_docker.sh` script. You need to create and login to your own Docker Hub account for this to work. Adapt the DOCKER_USERNAME, REPOSITORY_NAME and VERSION variables for your own docker user. You can then run the script in the terminal with `/.build_push_docker.sh`. 
   - If everything worked well, your container should become available on the Docker Hub, similar to this [example docker hub repo](https://hub.docker.com/repository/docker/moritzlaurer/litserve-huggingface-ie-siglip/general) for the SigLIP container. 

6. Once the container is successfully built and pushed to Docker Hub, you can deploy it to Hugging Face Endpoints. This is implemented in the `deploy.py` file for the example SigLIP container. Adapt the IMAGE_URL etc. accordingly for your own container image. You can then run this script in the terminal with `python deploy.py`. Note that the script assumes that you have a `.env` file with your own Hugging Face API key in the HF_TOKEN variable.

7. If everything worked well, you should then see your endpoint being initialized at https://endpoints.huggingface.co/. 

8. Once the endpoint is successfully initialized, you can make requests to it. You can make requests similar to the examples in the `client.py` or `client_async.py` files, only that you need to replace the local endpoint (http://0.0.0.0:8080/predict) with the endpoint URL, which you can find in the endpoint interface. Your endpoint url should look something like `https://n3sawwkbgf04ooqp.us-east-1.aws.endpoints.huggingface.cloud` + `/predict`.


## Other

### When not to use LitServe
LitServe is very flexible/general and can run any AI model. The main disadvantage of this is that it is less optimized for specific model types. If you want to serve generative LLMs, it is recommended to use [TGI](https://huggingface.co/docs/text-generation-inference/index) containers (the default on HF Endpoints, [docs](https://huggingface.co/docs/inference-endpoints/main/en/others/container_types#text-generation-inference)) or [vLLM](https://github.com/vllm-project/vllm) containers (can be deployed on HF endpoints following [this guide](https://github.com/MoritzLaurer/vllm-huggingface)). For serving text embedding or text classifier models, the default recommended containers for HF Endpoints are [TEI](https://huggingface.co/docs/text-embeddings-inference/quick_tour) containers.

LitServe does not use optimizations like torch.compile or flash-attention out of the box and these need to be implemented manually in the `server.py` file by the user. The correct implementation of these optimizations depends on the model and the hardware it is running on.


### When to use LitServe

LitServe is interesting for model types that are not supported by the specialized containers mentioned above. Examples include: image embeddings/segmentation/classification, or audio models (text-to-speech, speech-to-text, etc.).

Note that you can also deploy any Transformer model with a custom handler instead of using LitServe containers ([docs](https://huggingface.co/docs/inference-endpoints/guides/custom_handler)). I have not compared the performance of LitServe containers vs. the custom handler approach, but I expect LitServe containers to be faster (although more complex to set up). User feedback on this is welcome!


