import json

def json_to_ttl(json_file, ttl_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(ttl_file, 'w', encoding='utf-8') as f:
        f.write("@prefix ex: <http://example.org/> .\n")
        f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
        f.write("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n")
        f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
        f.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n")
        

        # ?  Definição das Data Properties
        f.write("###  http://example.org/temNome\n")
        f.write("ex:temNome rdf:type owl:DatatypeProperty ;\n")
        f.write("          rdfs:domain ex:Atleta ;\n")
        f.write("          rdfs:range xsd:string .\n\n")
        
        f.write("###  http://example.org/temModalidade\n")
        f.write("ex:temModalidade rdf:type owl:DatatypeProperty ;\n")
        f.write("          rdfs:domain ex:Atleta ;\n")
        f.write("          rdfs:range xsd:string .\n\n")
        
        f.write("###  http://example.org/temResultado\n")
        f.write("ex:temResultado rdf:type owl:DatatypeProperty ;\n")
        f.write("          rdfs:domain ex:Atleta ;\n")
        f.write("          rdfs:range xsd:string .\n\n")
        
        for entry in data:
            nome_completo = f"{entry['nome']['primeiro']} {entry['nome']['último']}"
            modalidade = entry['modalidade'].replace(" ", "_")
            resultado = "Saudavel" if entry['resultado'] else "NaoSaudavel"
            
            f.write(f"ex:{nome_completo.replace(' ', '_')} rdf:type ex:Atleta ;\n")
            f.write(f"    ex:temNome \"{nome_completo}\"^^xsd:string ;\n")
            f.write(f"    ex:temModalidade \"{modalidade}\"^^xsd:string ;\n")
            f.write(f"    ex:temResultado \"{resultado}\"^^xsd:string .\n\n")
            
            f.write(f"ex:{modalidade} rdf:type ex:Modalidade .\n\n")
            
            f.write(f"ex:{resultado} rdf:type ex:Resultado .\n\n")

json_to_ttl("emd.json", "emd.ttl")
