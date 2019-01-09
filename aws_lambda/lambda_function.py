
import boto3
#import s3fs
import json
import logging
import numpy as np
import pickle




def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin' : '*' #Required for CORS support to work
        },
    }


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    '''

    operations = {
        'POST': 'post_method()',
        'GET':''
    }

    operation = event['httpMethod']
    if operation in operations:
            
        if operation == 'POST':
            json_data = json.loads(event['body'])
            feature_names = ['gmat','gpa','']
            for feature in feature_names:
                pass
        elif operation == 'GET':
            print('**hit it fine**')

    return respond(None,{'good':'good'})

           