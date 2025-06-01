import csv
import shutil
from rdflib import Graph, URIRef, Literal, Namespace


#novo_ficheiro = "worldcup_relacoes.ttl"
#shutil.copy2("worldcup_povoada.ttl", novo_ficheiro)

g = Graph()
g.parse("worldcup_povoado.ttl", format="turtle")


def norm(x):
    return x.replace(" ", "_").replace("'", "_").replace('"', "_").replace("(", "_").replace(")", "_").replace("-", "_").replace(".", "_").replace(",", "_").replace(":", "_").replace(";", "_").replace("/", "_").replace("\\", "_").replace("?", "_").replace("!", "_").replace("&", "_").replace("%", "_").replace("$", "_").replace("#", "_").replace("@", "_").replace("=", "_").replace("+", "_").replace("*", "_").replace("<", "_").replace(">", "_").replace("  ", "_").replace(" ", "_")

n = Namespace("http://www.semanticweb.org/cid34senhas/ontologies/world_cup#")


## contar triplos 

def contar_triplos(g):
    count = 0
    for s, p, o in g:
        count += 1
    return count




def propriedades_sem_uso(g):
    # Lista todas as propriedades definidas como DatatypeProperty ou ObjectProperty
    propriedades = set()
    for s, p, o in g.triples((None, None, None)):
        if o in [URIRef("http://www.w3.org/2002/07/owl#DatatypeProperty"), URIRef("http://www.w3.org/2002/07/owl#ObjectProperty")]:
            propriedades.add(s)

    # Agora verifica se cada propriedade aparece como predicado em algum triplo
    nao_usadas = []
    for prop in propriedades:
        usada = False
        for s, p, o in g.triples((None, prop, None)):
            usada = True
            break
        if not usada:
            nao_usadas.append(prop)
    return nao_usadas

nao_usadas = propriedades_sem_uso(g)
print("Propriedades não usadas:")
for prop in nao_usadas:
    print(prop)


with open("squads.csv") as f:
    reader = csv.DictReader(f)
    teams = set()
    for row in reader:
        # Descobre o gênero pelo nome do torneio
        tournament = row["tournament_name"].lower()
        if "women" in tournament:
            gender = "woman"
        elif "men" in tournament:
            gender = "man"
        else:
            gender = "unknown"
        # Monta o id da equipa

        team_id = norm(f"{row['team_name']}_{gender}_{row['tournament_id']}")
        country_id = norm(row["team_name"])
        torneio_id = norm(row["tournament_name"])

        if team_id not in teams:
            teams.add(team_id)
            #print(f"Adicionando equipa: {team_id}")
            g.add((n[team_id], URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), n.Team))
            g.add((n[team_id], n["representaPais"], n[country_id]))
            g.add((n[team_id],n["participaEmTorneio"] ,n[torneio_id]))
        
        given_name = row['given_name'] if row['given_name'].lower() != 'not applicable' else ''
        family_name = row['family_name'] if row['family_name'].lower() != 'not applicable' else ''
        given_name = norm(given_name)
        family_name = norm(family_name)
        jogador_id = f"{given_name}_{family_name}"
        g.add((n[team_id], n["temJogador"], n[jogador_id]))
        g.add((n[jogador_id], n["pertenceaEquipa"], n[team_id]))
        
with open("referee_appointments.csv") as f:
    reader = csv.DictReader(f)
   
    for row in reader:
        arbitro_id = norm(f"{row['given_name']}_{row['family_name']}")
        torneio_id = norm(row["tournament_name"])

with open("referee_appearances.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        arbitro_id = norm(f"{row['given_name']}_{row['family_name']}")
        match_id = norm(f"{row['match_name']}_{row['match_id']}")
        g.add((n[arbitro_id], n["arbitrouPartida"], n[match_id]))
        g.add((n[match_id], n["temArbitro"], n[arbitro_id]))

with open("manager_appointments.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Determina o gênero pelo nome do torneio
        tournament = row["tournament_name"].lower()
        if "women" in tournament:
            gender = "woman"
        elif "men" in tournament:
            gender = "man"

        team_id = norm(f"{row['team_name']}_{gender}_{row['tournament_id']}")
        given_name = row['given_name'] if row['given_name'].lower() != 'not applicable' else ''
        family_name = row['family_name'] if row['family_name'].lower() != 'not applicable' else ''
        given_name = norm(given_name)
        family_name = norm(family_name)
        manager_id = norm(f"{given_name}_{family_name}")
        g.add((n[team_id], n["temTreinador"], n[manager_id]))
        g.add((n[manager_id], n["treinaEquipa"], n[team_id]))


with open("goals.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        match_id = norm(f"{row['match_name']}_{row['match_id']}")
        jogador_id = norm(f"{row['given_name']}_{row['family_name']}")
        g.add((n[match_id], n["goloMarcadoPor"], n[jogador_id]))
        g.add((n[jogador_id], n["marcouGoloEm"], n[match_id]))







g.serialize(destination="worldcup_relacoes.ttl", format="turtle")

print("Total de triplos:", contar_triplos(g))

