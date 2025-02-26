import boto3
import time
import json
from googlesearch import search

dynamodb = boto3.resource('dynamodb')

def clean_table(table):
    response = table.scan()
    for item in response.get('Items', []):
        table.delete_item(Key={'url': item['url']})
       

def lambda_handler(event, context):
    body = event.get('body', '{}')
    data = json.loads(body)
    city = data.get('city', None)

    table_name = 'all-url-table'
    table = dynamodb.Table(table_name)
    clean_table(table)
    all_url = []

    for url in search(f"inurl:{city}", num_results=5, lang="fr"):
        try:
            time.sleep(2)
            all_url.append(url)

            response = table.put_item(
                Item={
                    'id': str(hash(url)),
                    'url': url,
                }
            )
            print(f"Ajouté URL: {url}, Réponse DynamoDB: {response}")
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'URL: {url}, Erreur: {str(e)}")

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps({
            'urls': all_url
        })
    }
