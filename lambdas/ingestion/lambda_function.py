import json
import boto3
import pprint as pp
import time

bedrock_agent_client = boto3.client('bedrock-agent')

def lambda_handler(event, context):
    # TODO implement
    try :
        start_job_response = bedrock_agent_client.start_ingestion_job(knowledgeBaseId = "NO4BARBC7D", dataSourceId = "BMPT5STFUU")
        job = start_job_response["ingestionJob"]
        # Get job 
        while(job['status']!='COMPLETE' ):
            get_job_response = bedrock_agent_client.get_ingestion_job(
            knowledgeBaseId = "NO4BARBC7D",
            dataSourceId = "BMPT5STFUU",
            ingestionJobId = job["ingestionJobId"]
        )
        job = get_job_response["ingestionJob"]
        if(job['status']=='COMPLETE'):
            print("Ingestion Job Completed")
            
        pp.pprint(job)
        return {'statusCode': 200, 'body': json.dumps('Hello from Lambda!')}
    except Exception as e:
        return {'statusCode': 500, 'error': str(e)}
