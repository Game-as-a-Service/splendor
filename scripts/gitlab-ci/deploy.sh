#!/bin/bash

echo "$CI_COMMIT_REF_NAME"
case "$CI_COMMIT_REF_NAME" in
dev)
  HOST="$DEV_HOST"
  REDIS_HOST="$DEV_REDIS_HOST"
  ;;
uat)
  HOST="$UAT_HOST"
  REDIS_HOST="$UAT_REDIS_HOST"
  ;;
master)
  HOST="$MASTER_HOST"
  REDIS_HOST="$MASTER_REDIS_HOST"
  ;;
esac

USER="$USER"
eval $(ssh-agent -s)
ssh-add <(echo "$SSH_PRIVATE_KEY")


ssh -o StrictHostKeyChecking=no "${USER}@${HOST}" "ls -al"
ssh -o StrictHostKeyChecking=no "${USER}@${HOST}" "export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID &&
                                                   export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY &&
                                                   export AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION &&
                                                   aws ecr get-login-password --region $AWS_DEFAULT_REGION | sudo docker login --username AWS --password-stdin $DOCKER_REGISTRY &&
                                                   sudo docker pull $DOCKER_REGISTRY/$APP_NAME:$CI_COMMIT_REF_NAME &&
                                                   sudo docker ps -q --filter "name=$APP_NAME" | grep -q . && sudo docker stop $APP_NAME && sudo docker rm -fv $APP_NAME
                                                   sudo docker run -d --restart=always --name $APP_NAME -p 8888:5000 $DOCKER_REGISTRY/$APP_NAME:$CI_COMMIT_REF_NAME &&
                                                   sudo docker image prune -a --force
                                                   "

redis-cli -h ${REDIS_HOST} -p $REDIS_PORT -a $REDIS_PASSWORD -n 10 flushdb