# URL Shortener
A very rudimentary URL shortener built in Flask and DynamoDB.
This project serves as a way for myself to practice working with the Boto3 API and is not a perfect solution.

## Requirements
- Python3
- Flask
- Docker
- AWS DynamoDB

## Installation
The application depends on a few things to be set before it can be run. You need some environment variables set:

Begin by setting the app secret key. On MacOS and Linux this can be done:
```bash
export SECRET_KEY=REPLACE WITH A RANDOM STRING
```

We also need to set the DynamoDB endpoint if you are working with the local development image. If you have an AWS profile configured
for your region and wish to use it online, you can skip this step and just use the AWS profile instead.
```bash
export ENDPOINT_URL=http://localhost:8000
```

