# import decimal
import boto3
import json

from boto3.dynamodb.conditions import Key

import conf


CLIENT = boto3.resource('dynamodb')
TABLE_NAME = 'paycheck'

def query_by_emp_no(emp_no):
    table = CLIENT.Table(TABLE_NAME)
    response = table.query(
        # KeyConditionExpression = Key('emp_no').eq(emp_no)
        KeyConditionExpression = Key('emp_no').eq(emp_no) & Key('paid_date').gt('2019-10-01')
    )

    items = response['Items']
    # for item in items:
    #     print(item)
    return items

def lambda_handler(event, context):
    # TODO: Replace EMP_NO with actual value when applying to Lambda.
    items = query_by_emp_no(conf.EMP_NO)


    return 'Hello from Lambda'  