
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Chicago

WORKDIR /toolchain

RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    git \
    ca-certificates \ 
    zip \
    build-essential \
    cmake \
    g++ \
    clang \
    llvm \
    lld

COPY ./ .