import boto3
import urllib3
from bs4 import BeautifulSoup
import json

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def clean_s3_bucket(bucket_name):
    objects = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in objects:
        delete_objects = {'Objects': [{'Key': obj['Key']} for obj in objects['Contents']]}
        s3.delete_objects(Bucket=bucket_name, Delete=delete_objects)

def take_url_fromDb():
    table_name = 'all-url-table'
    table = dynamodb.Table(table_name)   
    response = table.scan()
    all_urls = [item['url'] for item in response.get('Items', []) if 'url' in item]
    return all_urls

def scrape_page(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    if response.status != 200:
        raise Exception(f"Erreur {response.status} lors de l'accès à {url}")
    soup = BeautifulSoup(response.data, 'html.parser')
    all_text = [line.strip() for line in soup.text.splitlines() if line.strip()]
    return all_text

def save_to_s3(datas, url):
    bucket_name = 'scrapping-data-bucket'
    s3.put_object(
            Bucket=bucket_name,
            Key=url,
            Body=json.dumps(datas),
            ContentType='application/json'
    )

def lambda_handler(event, context):
    try:
        clean_s3_bucket('scrapping-data-bucket')
        all_url = take_url_fromDb()
        for i, url in enumerate(all_url):
            data = scrape_page(url)
            save_to_s3(data, str(i))

        return {"statusCode": 200}
    except Exception as e:
        return {'statusCode': 500, 'error': str(e)}
