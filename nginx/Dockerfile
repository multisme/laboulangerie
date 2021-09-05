FROM registry.gitlab.com/tezos/flextesa:master-run
# Copy sandbox script
COPY test_sandbox.sh .
RUN apk update
# Set up nginx
RUN apk add nginx
COPY nginx.conf /etc/nginx
RUN nginx

ARG POETRY_VERSION=1.1.4

# Install poetry
RUN apk add --no-cache \
        curl \
        gcc \
        libressl-dev \
        musl-dev \
        libffi-dev && \
        poetry
RUN mkdir baker
COPY baker baker
WORKDIR baker
RUN poetry install --no-dev
#RUN apt-get -y install software-properties-common  libsodium-dev libsecp256k1-dev libgmp-dev git gcc pkg-config wget
#RUN add-apt-repository ppa:deadsnakes/ppa
# Install py39 from deadsnakes repository
#RUN apt-get install python3-9
# Install pip from standard ubuntu packages
#RUN apt-get install python3-pip

#RUN pip3 install poetry

#RUN poetry config virtualenvs.create false

#RUN poetry install --no-dev --no-root

