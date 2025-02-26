import json


import csv
import json
import pandas as pd

#LES LIENS
json_url="donnee.json"
csv_filename = "the_output.csv"

## OUVERTURE JSON
with open(json_url,'r',encoding="utf-8") as file:
    data=json.load(file)




# Écriture du fichier CSV
with open(csv_filename, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    
    # En-tête du fichier CSV
    writer.writerow(["Titre", "Donnée 1", "Donnée 2", "Donnée 3"])
    
    for key, values in data.items():
        if isinstance(values, list):  # Si c'est une liste, on écrit toutes les valeurs sur une seule ligne
            writer.writerow([key] + values)
        else:  # Si c'est une simple chaîne, on l'écrit seule sur la ligne
            writer.writerow([key, values])

print("fichier bien généré")



def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
