# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import boto3


def lambda_handler(event, context):
    print ("====================Lambda Start====================")

    table = boto3.client('dynamodb')

    table.put_item(
        Item={
            'device_id': 'zrgtest120501',
            'dsn': 'zrgtest120501',
            'product_id': 'zrgtest120501',
        }
    )

    response = table.get_item(
        Key={
            'product_id': 'zrgtest120501',
            'dsn': 'zrgtest120501'
        }
    )
    item = response['Item']
    print(item)
