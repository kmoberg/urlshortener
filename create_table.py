# Amazon DynamoDB Option
import boto3


def create_urls_table(dynamodb=None):
    # Get the service
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

    # Create the DynamoDB Table
    table = dynamodb.create_table(
        TableName = 'urls',
        KeySchema=[
            {
                'AttributeName': 'short_url',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'short_url',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


if __name__ == '__main__':
    device_table = create_urls_table()
    print("Status: ", device_table.table_status)
