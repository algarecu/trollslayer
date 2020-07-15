#!/bin/bash
imageName=$1
containerName=$2

docker build -t $imageName -f Dockerfile  .

echo Delete old container...
docker rm -f $containerName

echo Run new container...
docker run -d -P --name $containerName $imageName
