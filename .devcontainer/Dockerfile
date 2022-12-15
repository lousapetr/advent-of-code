FROM --platform=linux/amd64 ubuntu:20.04

SHELL ["/bin/bash", "-c"]
ENV BASH_ENV ~/.bashrc

# set up local time zone (e.g. to avoid interactive prompt during nodejs installation)
ENV TZ=Europe/Prague
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install basic packages
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends \
    git \
    wget \
    g++ \
    ca-certificates \
    build-essential \
    python3.10 \
    python-is-python3 \
    python3-pip \
    &&  rm -rf /var/lib/apt/lists/*


# Copy python requirements and install python libraries
COPY requirements.txt /

RUN python -m pip install -r requirements.txt
