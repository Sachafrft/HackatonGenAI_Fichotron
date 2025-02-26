import boto3
import json
import time
import pprint as pp
import os

# Créez le client Bedrock dans la région appropriée
bedrock_client = boto3.client('bedrock-agent-runtime', region_name='us-west-2')
s3 = boto3.client('s3')


# Préparez la charge utile (payload) telle que définie dans le JSON
# payload = {
#     "input": {
#         "text": "Quelle est la plus grande ville d'ile de france ? et parle moi un peu de ce departement."
#     },
#     "retrieveAndGenerateConfiguration": {
#         "knowledgeBaseConfiguration": {
#             "knowledgeBaseId": "NO4BARBC7D",
#             "modelArn": "mistral.mistral-large-2407-v1:0"
#         },
#         "type": "KNOWLEDGE_BASE"
#     }
# }


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    

# CALL LLM

def call_llm_api(query):
    payload = {
        "input": {
            "text": query
        },
        "retrieveAndGenerateConfiguration": {
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": "NO4BARBC7D",
                "modelArn": "mistral.mistral-large-2407-v1:0"
            },
            "type": "KNOWLEDGE_BASE"
        }
    }
    # pp.pprint(query)
    response = bedrock_client.retrieve_and_generate(**payload)
    return response['output']['text']

def create_json(file_path, data):
    tmp_file_path = os.path.join('/tmp', os.path.basename(file_path))
    with open(tmp_file_path, 'w') as f:
        json.dump(data, f, indent=4)
        
def save_to_s3(datas, nom):
    bucket_name = 'final-bucket-llamazing'
    s3.put_object(
            Bucket=bucket_name,
            Key=nom,
            Body=json.dumps(datas),
            ContentType='application/json'
    )
        
def get_prompt(path):
    with open(path, 'r') as f:
        return f.read()

def get_all_json_files(data_collectivite, data_metropole):
    
    list_prompts = []
    directory = './data/prompts'
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                content = file.read()
                list_prompts.append(content)

    listresult = []
    for i in list_prompts:
        listresult.append(call_llm_api(i))

    save_to_s3(listresult, "result")
       

    # # Finances de la collectivité
    # prompt = get_prompt("data/prompts/finances_collectivite.txt")
    # save_to_s3(call_llm_api(prompt), "finances_collectivite")
    
    # # Présentation de la collectivité
    # prompt = get_prompt("data/prompts/presentation_collectivite.txt")
    # save_to_s3(call_llm_api(prompt), "presentation_collectivite")
    
    # # Projets verts de la collectivité
    # prompt = get_prompt("data/prompts/projets_verts_collectivite.txt")
    # save_to_s3(call_llm_api(prompt), "projets_verts_collectivite")
    
    # # Projets sociaux de la collectivité
    # prompt = get_prompt("data/prompts/projets_sociaux_collectivite.txt")
    # save_to_s3(call_llm_api(prompt), "projets_sociaux_collectivite")
    
    # # Représentant de la collectivité
    # prompt = get_prompt("data/prompts/representant_collectivite.txt")
    # pp.pprint(f"SALUT{call_llm_api(prompt)}")
    # save_to_s3(call_llm_api(prompt), "representant_collectivite")
    
    # # Budget de la collectivité
    # prompt = get_prompt("data/prompts/budget_collectivite.txt")
    # create_json(data_collectivite['budget_collectivite'], call_llm_api(prompt))
    
    # # A une métropole
    # prompt = get_prompt("data/prompts/has_a_metropole.txt")
    # create_json(data_collectivite['has_a_metropole'], call_llm_api(prompt))
    
    
    # ### METROPOLE ###
    
    # # Finances de la métropole
    # prompt = get_prompt("data/prompts/finances_metropole.txt")
    # create_json(data_metropole['finances_metropole'], call_llm_api(prompt))
    
    # # Présentation de la métropole
    # prompt = get_prompt("data/prompts/presentation_metropole.txt")
    # create_json(data_metropole['presentation_metropole'], call_llm_api(prompt))
    
    # # Projets verts de la métropole
    # prompt = get_prompt("data/prompts/projets_verts_metropole.txt")
    # create_json(data_metropole['projets_verts_metropole'], call_llm_api(prompt))
    
    # # Projets sociaux de la métropole
    # prompt = get_prompt("data/prompts/projets_sociaux_metropole.txt")
    # create_json(data_metropole['projets_sociaux_metropole'], call_llm_api(prompt))
    
    # # Représentant de la métropole
    # prompt = get_prompt("data/prompts/representant_metropole.txt")
    # create_json(data_metropole['representant_metropole'], call_llm_api(prompt))
    
    # # Budget de la métropole
    # prompt = get_prompt("data/prompts/budget_metropole.txt")
    # create_json(data_metropole['budget_metropole'], call_llm_api(prompt))



def lambda_handler(event, context):   
    data_collectivite = {
        'logo_collectivite': "data/raw/logo_collectivite.json",
        'finances_collectivite': "data/raw/finances_collectivite.json",
        'presentation_collectivite': "data/raw/presentation_collectivite.json",
        'projets_verts_collectivite': "data/raw/projets_verts_collectivite.json",
        'projets_sociaux_collectivite': "data/raw/projets_sociaux_collectivite.json",
        'representant_collectivite': "data/raw/representant_collectivite.json",
        'budget_collectivite': "data/raw/budget_collectivite.json",
        'has_a_metropole': "data/raw/has_a_metropole.json",
    }
    
    data_metropole = {
        'finances_metropole': "data/raw/finances_metropole.json",
        'presentation_metropole': "data/raw/presentation_metropole.json",
        'projets_verts_metropole': "data/raw/projets_verts_metropole.json",
        'projets_sociaux_metropole': "data/raw/projets_sociaux_metropole.json",
        'representant_metropole': "data/raw/representant_metropole.json",
        'budget_metropole': "data/raw/budget_metropole.json",
    }

    get_all_json_files(data_collectivite, data_metropole)


    # response = bedrock_client.retrieve_and_generate(**payload)

    # Affichez la réponse (formatée en JSON pour une meilleure lisibilité)
    # print(json.dumps(response, indent=4))

    return {
        "statusCode": 200,
        # "body": json.dumps({
        #     "answer": response
        # })
    }