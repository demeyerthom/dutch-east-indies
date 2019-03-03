#!/usr/bin/env bash

docker build --tag demeyerthom/dutch-east-indies-convert:latest  --file deployments/docker/Dockerfile.convert .

docker stop dutch-east-indies-convert || true && docker rm dutch-east-indies-convert || true

docker run --name dutch-east-indies-convert -d \
    --network=production \
    --volume /data/dutch-east-indies/sources/books:/data/books \
    --volume /data/dutch-east-indies/sources/processed:/data/processed \
    --env OCR_KEY=a9f48e6f4e88957 \
    --env NUMBER=500 \
    demeyerthom/dutch-east-indies-convert:latest