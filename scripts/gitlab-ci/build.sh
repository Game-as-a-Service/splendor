#!/bin/bash

echo "$CI_COMMIT_REF_NAME"
case "$CI_COMMIT_REF_NAME" in
dev)
  WORKER=2
  ;;
uat)
  WORKER=4
  ;;
master)
  WORKER=4
  ;;
esac


sudo docker build \
    --build-arg BRANCH=$CI_COMMIT_BRANCH \
    --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    --build-arg WORKER=${WORKER} \
    -t $DOCKER_REGISTRY/$APP_NAME:$CI_COMMIT_BRANCH . --no-cache
aws ecr get-login-password --region $AWS_DEFAULT_REGION | sudo docker login --username AWS --password-stdin $DOCKER_REGISTRY
sudo docker push $DOCKER_REGISTRY/$APP_NAME:$CI_COMMIT_BRANCH