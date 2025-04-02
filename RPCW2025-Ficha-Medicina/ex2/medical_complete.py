import csv 
import json 
import shutil 
symptom_list = []
disease_symptoms = {}
treatments_list = []
diasease_treatments = {}
#shutil.copy2("medical.ttl", "med_doencas.ttl")

#shutil.copy2("medical.ttl", "med_tratamentos.ttl")
shutil.copy2("medical.ttl", "med_doentes.ttl")




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

        

with open("Disease_Treatment.csv", "r") as fin:
    reader = csv.DictReader(fin)
    #print(reader.fieldnames)
    for row in reader:
        disease = row["Disease"]
        treatments = set()
        
        # Coletar todos os tratamentos não vazios da linha (Treatment_1 a Treatment_17)
        for i in range(1, 4):
            treatment = row.get(f"Precaution_{i}", "").strip()
            if treatment:  # Ignora strings vazias
                treatment = treatment.replace(" ", "_")
                treatment = treatment.replace("(", "_")
                treatment = treatment.replace(")", "_")
                treatments.add(treatment)
                if treatment not in treatments_list:
                    treatments_list.append(treatment)
        
        # Atualiza o dicionário: se a doença já existe, adiciona novos tratamentos
        if disease:
            disease = disease.replace(" ", "_")
            disease = disease.replace("(", "_")
            disease = disease.replace(")", "_")
        if disease in diasease_treatments:
            diasease_treatments[disease].update(treatments)
        else:
            diasease_treatments[disease] = treatments


#print(disease_symptoms)

# Exemplo 
#:Flu a :Disease ;
#   :hasSymptom :Fever, :Cough, :SoreThroat ;

#print(diasease_treatments)

symptom_data = ""
for symptom in symptom_list:
    symptom_data += f""":{symptom} a :Symptom.\n"""

treatments_data = ""
for treatment in treatments_list:
    treatments_data += f""":{treatment} a :Treatment.\n"""

diasease_data = ""
for disease, symptoms in disease_symptoms.items():
    #treatments = diasease_treatments.get(disease, set())  
    diasease_data += f""":{disease} a :Disease ;
        :hasSymptom {", ".join([f":{s}" for s in symptoms])} ;
        :hasTreatment {", ".join([f":{t}" for t in treatments])}.\n"""


with open("doentes.json", "r") as json_file:
    patients_data = json.load(json_file)

# Gerar os dados no formato especificado
patients_output = ""
for idx, patient in enumerate(patients_data, start=1):
    patient_name = patient.get("nome", "Unknown").replace('"', '\\"')  # Escapar aspas duplas no nome
    symptoms = patient.get("sintomas", [])
    patients_output += f""":Patient{idx} a :Patient ;
    :name "{patient_name}" ;
"""
    for symptom in symptoms:
        symptom = symptom.replace(" ", "_").replace("(", "_").replace(")", "_")
        patients_output += f"    :exhibitsSymptom :{symptom} ;\n"
    patients_output = patients_output.rstrip(" ;\n") + " .\n"  # Remover o último ponto e vírgula e adicionar ponto final
# Print the generated data
#print(symptom_data)
#print(diasease_data)
# Output the data to a file
with open("med_doentes.ttl", "a") as f:
    f.write(symptom_data)
    f.write(treatments_data)
    f.write(diasease_data)
    f.write(patients_output)
   


