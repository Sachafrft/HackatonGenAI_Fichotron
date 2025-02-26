import boto3

# Utilisez le client "bedrock-agent-runtime" au lieu de "bedrock-runtime"
client = boto3.client("bedrock-agent-runtime", region_name="us-west-2")  # Oregon

# Appelez retrieve_and_generate avec les paramètres adaptés
response = client.retrieve_and_generate(
    input={
        "text": "Votre question ou requête ici"
    },
    retrieveAndGenerateConfiguration={
        "type": "KNOWLEDGE_BASE",  # Indique que l'on utilise une base de connaissances
        "knowledgeBaseConfiguration": {
            "knowledgeBaseId": "NO4BARBC7D",  # Votre ID de Knowledge Base
            "modelArn": "arn:aws:bedrock:us-west-2::model/anthropic.claude-v2"
        }
    }
)

print(response["output"]["text"])
