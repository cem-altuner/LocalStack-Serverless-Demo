import json
import time
import logging
import os
import boto3

if 'LOCALSTACK_HOSTNAME' in os.environ:
    dynamodb_endpoint = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint)
else:
    dynamodb = boto3.resource('dynamodb')


def updateCustomer(event, context):
    data = json.loads(event['body'])
    if 'firstName' not in data:
        logging.error("Validation Error")
        raise Exception("Couldn't update the Customer item.")

    timestamp = str(time.time())

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # update the Customer in the database
    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
          '#firstName': 'firstName',
        },
        ExpressionAttributeValues={
          ':firstName': data['firstName'],
          ':lastName': data['lastName'],
          ':updatedAt': timestamp,
        },
        UpdateExpression='SET #firstName = :firstName, '
                         'lastName = :lastName, '
                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'])
    }

    return response