# URL Shortener
A very rudimentary URL shortener built in Flask and DynamoDB.
This project serves as a way for myself to practice working with the Boto3 API and is not a perfect solution.

## Requirements
- Python3
- Flask
- Docker
- AWS DynamoDB

## Installation
There are multiple ways to run this application. The best way is to run it in Docker, using the Dockerfile or better yet, the Docker-compose file.

### Running in Docker
Simple! If you have [Docker](https://docker.io) and Docker-Compose installed, run:
```bash
docker-compose up --build
```

The app should now be available at http://localhost:5000 with DynamoDB locally available at http://localhost:8000 (or http://dynamodb-local:8000 for other containers in the docker-compose environment).

### Running manually

The application depends on a few things to be set before it can be run. 

**IMPORTANT!** You must have either a set of real AWS credentials added to your path, or a set of fake ones. You can set the default region to `localhost` which will avoid any commands being sent to AWS. 

Additionally, you need some environment variables set:

Begin by setting the app secret key. On MacOS and Linux this can be done:
```bash
export SECRET_KEY=REPLACE WITH A RANDOM STRING
```

We also need to set the DynamoDB endpoint if you are working with the local development image. If you have an AWS profile configured
for your region and wish to use it online, you can skip this step and just use the AWS profile instead.
```bash
export ENDPOINT_URL=http://localhost:8000
# Note: If you're using docker-compose, the URL will be http://dynamodb-local:8000
```

You can now run the app using
```python
flask run
```
