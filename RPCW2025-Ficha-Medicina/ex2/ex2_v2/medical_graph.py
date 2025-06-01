from rdflib import Graph, URIRef,RDF
import csv 
from rdflib.namespace import FOAF , XSD

g = Graph()

g.parse("medical.ttl")






symptom_list = []
disease_symptoms = {}
treatments_list = []




with open("Disease_Syntoms.csv", "r") as fin:
    reader = csv.DictReader(fin)
    #print(reader.fieldnames)

    for row in reader:
        disease = row["Disease"]
        symptoms = set()
        
        # Coletar todos os sintomas não vazios da linha (Symptom_1 a Symptom_17)
        for i in range(1, 18):
            symptom = row.get(f"Symptom_{i}", "").strip()
            if symptom:  # Ignora strings vazias
                symptom = symptom.replace(" ", "_")
                symptom = symptom.replace("(", "_")
                symptom = symptom.replace(")", "_")
                symptoms.add(symptom)
                if symptom not in symptom_list:
                    symptom_list.append(symptom)
        
        # Atualiza o dicionário: se a doença já existe, adiciona novos sintomas
        if disease:
            disease = disease.replace(" ", "_")
            disease = disease.replace("(", "_")
            disease = disease.replace(")", "_")
        if disease in disease_symptoms:
            disease_symptoms[disease].update(symptoms)
        else:
            disease_symptoms[disease] = symptoms



ed = URIRef("http://rpcw.di.uminho.pt/2024/medical#")


for disease, symptoms in disease_symptoms.items():
    # Cria o URI para a doença
    disease_uri = URIRef(f"{ed}{disease}")
    # Adiciona a tripla indicando o tipo da doença
    g.add((disease_uri, RDF.type, URIRef(f"{ed}Disease")))
    
    # Supondo que 'symptoms' seja uma lista de sintomas para cada doença:
    for symptom in symptoms:
        symptom_uri = URIRef(f"{ed}{symptom}")
        g.add((disease_uri, URIRef(f"{ed}hasSymptom"), symptom_uri))

for symptom in symptom_list:
    # Normalizar o nome do sintoma para evitar caracteres inválidos
    symptom = symptom.replace(" ", "_").replace("(", "_").replace(")", "_")
    symptom_uri2 = URIRef(f"{ed}{symptom}")
    g.add((symptom_uri2, RDF.type, URIRef(f"{ed}Symptom")))



# Bind the FOAF namespace to a prefix for more readable output
g.bind("foaf", FOAF)

# print all the data in the Notation3 format
print(g.serialize(format='turtle'))
