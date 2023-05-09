#!/bin/bash 

# chmod +x build-push-image.sh
# usage: ./build-push-image.sh <desired tagged image> <directory in which the Dockerfile of service is located>
# example: ./build-push-image.sh jkoniusz/rsww-179919-api-gateway:v1 api_gateway

set -ex

if [ $# -eq 0 ]; then
  echo "Wrong usage"
  exit 1
fi

docker login
docker build -t $1 $2
docker push $1
