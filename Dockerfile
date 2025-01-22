# Change CUDA version to match HF Endpoints
FROM --platform=linux/amd64 nvidia/cuda:12.3.0-base-ubuntu22.04
ARG PYTHON_VERSION=3.11

ENV DO_NOT_TRACK=1

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        python${PYTHON_VERSION} \
        python${PYTHON_VERSION}-dev \
        python${PYTHON_VERSION}-venv \
        python3-pip \
        wget \
    && ln -sf /usr/bin/python${PYTHON_VERSION} /usr/bin/python3 \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip \
    && python --version \
    && pip --version \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy entrypoint script and set permissions
COPY --chmod=775 endpoints-entrypoint.sh /entrypoint.sh

WORKDIR /app
COPY . /app

# Install litserve and requirements
RUN pip install --no-cache-dir litserve==0.2.6 -r requirements.txt

# Verify CUDA availability
RUN python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('CUDA version:', torch.version.cuda)"

EXPOSE 8080

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
CMD [""]
