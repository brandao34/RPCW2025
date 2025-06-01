import csv
import shutil

novo_ficheiro = "worldcup_povoado.ttl"
shutil.copy2("base_completa.ttl", novo_ficheiro)

def norm(x):
    return x.replace(" ", "_").replace("'", "_").replace('"', "_").replace("(", "_").replace(")", "_").replace("-", "_").replace(".", "_").replace(",", "_").replace(":", "_").replace(";", "_").replace("/", "_").replace("\\", "_").replace("?", "_").replace("!", "_").replace("&", "_").replace("%", "_").replace("$", "_").replace("#", "_").replace("@", "_").replace("=", "_").replace("+", "_").replace("*", "_").replace("<", "_").replace(">", "_").replace("  ", "_").replace(" ", "_")

generic_properties = """
## 
:global_id rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:string .

:name rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:string .

:sex rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:string .

:wikipediaLink rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:string .

:capacity rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:integer .



:birthDate rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:date .

:position rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:string .

:countTournaments rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:integer .

:listTournaments rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:string .

:year rdf:type owl:DatatypeProperty ; rdfs:range xsd:integer .

:startDate rdf:type owl:DatatypeProperty ; rdfs:range xsd:date .

:endDate rdf:type owl:DatatypeProperty ; rdfs:range xsd:date .



:countTeams rdf:type owl:DatatypeProperty ; rdfs:range xsd:integer .

:teamCode rdf:type owl:DatatypeProperty ; rdfs:range xsd:string .

:teamType rdf:type owl:DatatypeProperty ; rdfs:range xsd:string .

:matchDate rdf:type owl:DatatypeProperty ; rdfs:range xsd:date .
:matchTime rdf:type owl:DatatypeProperty ; rdfs:range xsd:string .
:stageName rdf:type owl:DatatypeProperty ; rdfs:range xsd:string .
:groupName rdf:type owl:DatatypeProperty ; rdfs:range xsd:string .
:score rdf:type owl:DatatypeProperty ; rdfs:range xsd:string .
:homeTeamScore rdf:type owl:DatatypeProperty ; rdfs:range xsd:integer .
:awayTeamScore rdf:type owl:DatatypeProperty ; rdfs:range xsd:integer .





""" 
generic_properties_2 = """
:global_id rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:string .

:name rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:string .

:sex rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:string .

:wikipediaLink rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:string .

:capacity rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:integer .

:fromCountry rdf:type owl:ObjectProperty ;
    rdfs:range :Country .

:locatedInCity rdf:type owl:ObjectProperty ;
    rdfs:range :City .

:locatedInCountry rdf:type owl:ObjectProperty ;
    rdfs:range :Country .

:birthDate rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:date .

:position rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:string .

:countTournaments rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:integer .

:listTournaments rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:string .

:year rdf:type owl:DatatypeProperty ; rdfs:range xsd:integer .

:startDate rdf:type owl:DatatypeProperty ; rdfs:range xsd:date .

:endDate rdf:type owl:DatatypeProperty ; rdfs:range xsd:date .

:hostCountry rdf:type owl:ObjectProperty ; rdfs:range :Country .

:winner rdf:type owl:ObjectProperty ; rdfs:range :Country .

:countTeams rdf:type owl:DatatypeProperty ; rdfs:range xsd:integer .

:teamCode rdf:type owl:DatatypeProperty ; rdfs:range xsd:string .

:teamType rdf:type owl:DatatypeProperty ; rdfs:range xsd:string .

:matchDate rdf:type owl:DatatypeProperty ; rdfs:range xsd:date .
:matchTime rdf:type owl:DatatypeProperty ; rdfs:range xsd:string .
:stageName rdf:type owl:DatatypeProperty ; rdfs:range xsd:string .
:groupName rdf:type owl:DatatypeProperty ; rdfs:range xsd:string .
:score rdf:type owl:DatatypeProperty ; rdfs:range xsd:string .
:homeTeamScore rdf:type owl:DatatypeProperty ; rdfs:range xsd:integer .
:awayTeamScore rdf:type owl:DatatypeProperty ; rdfs:range xsd:integer .
:homeTeam rdf:type owl:ObjectProperty ; rdfs:range :Team .
:awayTeam rdf:type owl:ObjectProperty ; rdfs:range :Team .
:playedAtStadium rdf:type owl:ObjectProperty ; rdfs:range :Stadium .
:playedInTournament rdf:type owl:ObjectProperty ; rdfs:range :Tournament .




"""



cidades = {}
paises = {}
estadios = {}

# Construção dos estádios
with open("stadiums.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        sid = norm(row["stadium_id"])
        sname = norm(row["stadium_name"].replace('"', '\\"'))
        city = norm(row["city_name"])
        city_label = norm(row["city_name"].replace('"', '\\"'))
        country = norm(row["country_name"])
        country_label = norm(row["country_name"].replace('"', '\\"'))
        capacity = row["stadium_capacity"]
        wiki = row["stadium_wikipedia_link"].replace('"', '\\"')
        cidades[city] = city_label
        paises[country] = country_label
        estadios[sid] = {
            "global_id": sid,
            "name": sname,
            "city": city,
            "country": country,
            "capacity": capacity,
            "wikipediaLink": wiki
        }

estadios_ttl = ""
for cid, label in cidades.items():
    estadios_ttl += f':{cid} a :City .\n'

for est in estadios.values():
    estadios_ttl += f"""
:{est['name']} a :Stadium ;
    :global_id "{est['global_id']}" ;
    :name "{est['name']}" ;
    :capacity {est['capacity']} ;
    :wikipediaLink "{est['wikipediaLink']}" ;
    :locatedInCity :{est['city']} ;
    :locatedInCountry :{est['country']} .
"""

# Árbitros
arbitros = {}
with open("referees.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rid = norm(row["referee_id"])
        name = norm(f"{row['given_name']}_{row['family_name']}")
        sex = "feminino" if row["female"] == "1" else "masculino"
        country = norm(row["country_name"])
        country_label = norm(row["country_name"])
        wiki = row["referee_wikipedia_link"].replace('"', '\\"')
        paises[country] = country_label
        arbitros[rid] = {
            "global_id": rid,
            "name": name,
            "sex": sex,
            "country": country,
            "wikipediaLink": wiki
        }

arbitros_ttl = ""
for arb in arbitros.values():
    arbitros_ttl += f"""
:{arb['name']} a :Referee ;
    :global_id "{arb['global_id']}" ;
    :name "{arb['name']}" ;
    :sex "{arb['sex']}" ;
    :wikipediaLink "{arb['wikipediaLink']}" ;
    :fromCountry :{arb['country']} .
"""

# Treinadores
managers = {}
with open("managers.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        mid = norm(row["manager_id"])
        given_name = row['given_name'] if row['given_name'].lower() != 'not applicable' else ''
        family_name = row['family_name'] if row['family_name'].lower() != 'not applicable' else ''
        given_name = norm(given_name)
        family_name = norm(family_name)
        name = f"{given_name}_{family_name}".replace(" ", "_")
        sex = "feminino" if row["female"] == "1" else "masculino"
        country = norm(row["country_name"])
        country_label = norm(row["country_name"])
        wiki = row["manager_wikipedia_link"].replace('"', '\\"')
        paises[country] = country_label
        managers[mid] = {
            "global_id": mid,
            "name": name.replace(' ', '_'),
            "sex": sex,
            "country": country,
            "wikipediaLink": wiki
        }

managers_ttl = ""
for man in managers.values():
    managers_ttl += f"""
:{man['name']} a :Coach ;
    :global_id "{man['global_id']}" ;
    :name "{man['name']}" ;
    :sex "{man['sex']}" ;
    :wikipediaLink "{man['wikipediaLink']}" ;
    :fromCountry :{man['country']} .
"""

# Jogadores
players = {}
with open("players.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        pid = norm(row["player_id"])
        given_name = row['given_name'] if row['given_name'].lower() != 'not applicable' else ''
        family_name = row['family_name'] if row['family_name'].lower() != 'not applicable' else ''
        given_name = norm(given_name)
        family_name = norm(family_name)
        name = f"{given_name}_{family_name}".replace(" ", "_")
        sex = "feminino" if row["female"] == "1" else "masculino"
        birth_date = row["birth_date"] if row["birth_date"] != "not available" else ""
        wiki = row["player_wikipedia_link"].replace('"', '\\"')
        # Determinar posição
        positions = []
        if row["goal_keeper"] == "1":
            positions.append("goalkeeper")
        if row["defender"] == "1":
            positions.append("defender")
        if row["midfielder"] == "1":
            positions.append("midfielder")
        if row["forward"] == "1":
            positions.append("forward")
        position = ",".join(positions) if positions else "unknown"
        count_tournaments = row["count_tournaments"]
        list_tournaments = row["list_tournaments"].replace('"', '\\"')
        players[pid] = {
            "global_id": pid,
            "name": name.replace(' ', '_'),
            "sex": sex,
            "birthDate": birth_date,
            "position": position,
            "countTournaments": count_tournaments,
            "listTournaments": list_tournaments,
            "wikipediaLink": wiki
        }

players_ttl = ""
for p in players.values():
    players_ttl += f"""
:{p['name']} a :Player ;
    :global_id "{p['global_id']}" ;
    :name "{p['name']}" ;
    :sex "{p['sex']}" ;
    :birthDate "{p['birthDate']}" ;
    :position "{p['position']}" ;
    :countTournaments {p['countTournaments']} ;
    :wikipediaLink "{p['wikipediaLink']}" .
"""

# Torneios
tournaments = {}
with open("tournaments.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        tid = norm(row["tournament_id"])
        tname = norm(row["tournament_name"])
        year = row["year"]
        start_date = row["start_date"]
        end_date = row["end_date"]
        host_country = norm(row["host_country"])
        tournament = row["tournament_name"].lower()
        if "women" in tournament:
            gender = "woman"
        elif "men" in tournament:
            gender = "man"
        
        winner = f"{norm(row["winner"])}_{gender}_{norm(row['tournament_id'])}" 
        count_teams = row["count_teams"]
        tournaments[tid] = {
            "global_id": tid,
            "name": tname,
            "year": year,
            "startDate": start_date,
            "endDate": end_date,
            "hostCountry": host_country,
            "winner": winner,
            "countTeams": count_teams
        }
        paises[host_country] = host_country  # Garante que o país anfitrião está na ontologia

tournaments_ttl = ""
for t in tournaments.values():
    tournaments_ttl += f"""
:{t['name']} a :Tournament ;
    :global_id "{t['global_id']}" ;
    :name "{t['name']}" ;
    :year {t['year']} ;
    :startDate "{t['startDate']}" ;
    :endDate "{t['endDate']}" ;
    :hostCountry :{t['hostCountry']} ;
    :temVencedor :{t['winner']} ;
    :countTeams {t['countTeams']} .
"""

# Equipas (Teams)
teams = {}
with open("teams.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        tid = norm(row["team_id"])
        tname = norm(row["team_name"])
        team_code = row["team_code"]
        federation_name = norm(row["federation_name"])
        region_name = norm(row["region_name"])

        # Adiciona instância para equipa masculina, se existir
        if row["mens_team"] == "1":
            team_man_name = f"{tname}_man"
            team_man_wiki = row["mens_team_wikipedia_link"].replace('"', '\\"')
            teams[team_man_name] = {
                "global_id": tid,
                "name": team_man_name,
                "teamCode": team_code,
                "teamType": "man",
                "federationName": federation_name,
                "regionName": region_name,
                "teamWiki": team_man_wiki,
            }
        # Adiciona instância para equipa feminina, se existir
        if row["womens_team"] == "1":
            team_woman_name = f"{tname}_woman"
            team_woman_wiki = row["womens_team_wikipedia_link"].replace('"', '\\"')
            teams[team_woman_name] = {
                "global_id": tid,
                "name": team_woman_name,
                "teamCode": team_code,
                "teamType": "woman",
                "federationName": federation_name,
                "regionName": region_name,
                "teamWiki": team_woman_wiki,
            }

teams_ttl = ""
for t in teams.values():
    teams_ttl += f"""
:{t['name']} a :Team ;
    :global_id "{t['global_id']}" ;
    :name "{t['name']}" ;
    :teamCode "{t['teamCode']}" ;
    :teamType "{t['teamType']}" ;
    :wikipediaLink "{t['teamWiki']}" .
"""

country_ttl = ""
for pid, label in paises.items():
    country_ttl += f':{pid} a :Country .\n'

matches = {}
with open("matches.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        mid = norm(row["match_id"])
        mname = norm(row["match_name"])
        tournament = norm(row["tournament_name"])
        stage = norm(row["stage_name"])
        group = norm(row["group_name"])
        match_date = row["match_date"]
        match_time = row["match_time"]
        stadium = norm(row["stadium_name"])
        home_team = norm(f"{row['home_team_name']}_{'man' if 'man' in row['home_team_name'].lower() else 'woman'}_{row['tournament_id']}")  # ajuste se necessário
        away_team = norm(f"{row['away_team_name']}_{'man' if 'man' in row['away_team_name'].lower() else 'woman'}_{row['tournament_id']}")  # ajuste se necessário
        score = row["score"]
        home_team_score = row["home_team_score"]
        away_team_score = row["away_team_score"]

        matches[mid] = {
            "global_id": mid,
            "name": mname,
            "matchDate": match_date,
            "matchTime": match_time,
            "stageName": stage,
            "groupName": group,
            "score": score,
            "homeTeamScore": home_team_score,
            "awayTeamScore": away_team_score,
            "stadium": stadium,
            "tournament": tournament,
            "homeTeam": home_team,
            "awayTeam": away_team
        }

matches_ttl = ""
for m in matches.values():
    matches_ttl += f"""
:{m['name']}_{m['global_id']} a :Match ;
    :global_id "{m['global_id']}" ;
    :name "{m['name']}" ;
    :matchDate "{m['matchDate']}" ;
    :matchTime "{m['matchTime']}" ;
    :stageName "{m['stageName']}" ;
    :groupName "{m['groupName']}" ;
    :score "{m['score']}" ;
    :homeTeamScore {m['homeTeamScore']} ;
    :awayTeamScore {m['awayTeamScore']} ;
    :playedAtStadium :{m['stadium']} ;
    :playedInTournament :{m['tournament']} ;
    :homeTeam :{m['homeTeam']} ;
    :awayTeam :{m['awayTeam']} .
"""

with open(novo_ficheiro, "a") as f:
    f.write(generic_properties)
    f.write(country_ttl)
    f.write(estadios_ttl)
    f.write(arbitros_ttl)
    f.write(managers_ttl)
    f.write(players_ttl)
    f.write(tournaments_ttl)
  #  f.write(teams_ttl)
    f.write(matches_ttl)

print(f"Ontologia criada com sucesso em {novo_ficheiro}!")



