# Build stage
FROM --platform=linux/amd64 python:3.11-slim-bullseye AS builder

# Add build argument for GitHub token
ARG GITHUB_TOKEN
ARG VERSION="master"

ENV VERSION=${VERSION}

RUN echo ${VERSION}
RUN pip install --upgrade pip
# Install git
RUN apt-get update && apt-get install -y --no-install-recommends git build-essential && apt-get purge -y --auto-remove && rm -rf /var/lib/apt/lists/*

# Install source
RUN mkdir /src
WORKDIR /src
COPY ./app  app

# Configure git to use token
RUN git config --global url."https://${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"

# Clone your repository
WORKDIR /github
RUN git clone -b ${VERSION} https://github.com/airembr/sdk                    sdk
RUN cp -r /github/sdk/airembr            /src/airembr

WORKDIR /src
RUN pwd
RUN ls -al

# Virtual env
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:/src:$PATH"

RUN pip install wheel

# Install torch for CPU only (pinned for reproducible builds)
RUN pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu --no-deps

RUN pip --no-cache-dir --default-timeout=240 install -r app/requirements.txt
RUN pip --no-cache-dir --default-timeout=240 install -r airembr/sdk/requirements.txt

RUN pip list

# Final stage - token is not carried over to this stage
FROM --platform=linux/amd64 python:3.11-slim-bullseye
LABEL maintaner=admin@tracardi.com

RUN pip install --upgrade pip

# Virtual env
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:/src:$PATH"

RUN pip install --upgrade pip

WORKDIR /src

COPY --from=builder /src .
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

# Set a default value for TAG_VERSION
ARG IMAGE_TAG="latest"

ENV VARIABLE_NAME="application"

ENV IMAGE_TAG=${IMAGE_TAG}
ENV SERVER_LOGGING_LEVEL=warning
ENV PYTHONPATH="$VIRTUAL_ENV/bin:/src:$PYTHONPATH"
ENV PYTHONUNBUFFERED=1

# Cap CPU ISA dispatch to AVX2 to avoid SIGILL from AVX512/VNNI quantized kernels
# on older K8s nodes that don't support those instructions.
ENV ATEN_CPU_CAPABILITY=avx2
ENV DNNL_MAX_CPU_ISA=AVX2

#ENTRYPOINT ["python3", "app/main.py"]
CMD ["sh", "-c", "uvicorn app.main:application --proxy-headers --host 0.0.0.0 --port 80 --log-level $SERVER_LOGGING_LEVEL"]