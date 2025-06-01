from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
import random
import requests
import re 

app = Flask(__name__)
app.secret_key = 'FIFA World Cup Secret Key'
CORS(app)
MODOS = {
    "facil": {"total": 6, "min_acertos": 2, "nome": "Fácil"},
    "mediano": {"total": 8, "min_acertos": 5, "nome": "Mediano"},
    "expert": {"total": 12, "min_acertos": 10, "nome": "Expert"},
    "morte_subita": {"total": 9999, "min_acertos": 1, "nome": "Morte Súbita"}
}
GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/FifaWorldCup"

def query_graphdb(sparql_query):
    headers = {'Accept': 'application/json'}
    params = {'query': sparql_query}
    try:
        response = requests.get(GRAPHDB_ENDPOINT, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying GraphDB: {e}")
        return None

# ... (as tuas funções get_jogadores, get_tecnicos, etc. mantêm-se iguais) ...

@app.route('/')
def home():
    session['score'] = 0
    modos_concluidos = session.get('modos_concluidos', [])
    maior_score = session.get('maior_score', 0)
    return render_template('home.html', modos_concluidos=modos_concluidos, maior_score=maior_score)

@app.route('/temas', methods=['GET'])
def temas():
    modo = request.args.get('modo')
    if not modo:
        return redirect(url_for('home'))
    session['modo'] = modo  # Guarda o modo na sessão
    return render_template('temas.html', modo=modo)

def get_jogadores():
    sparql = """
    PREFIX : <http://www.semanticweb.org/cid34senhas/ontologies/world_cup#>
    SELECT ?nome ?nascimento ?posicao WHERE {
      ?jogador a :Player ;
               :name ?nome ;
               :birthDate ?nascimento ;
               :position ?posicao .
    }
    """
    results = query_graphdb(sparql)
    if not results: return []
    return [
        {
            "nome": r["nome"]["value"],
            "nascimento": r["nascimento"]["value"],
            "posicao": r["posicao"]["value"]
        }
        for r in results["results"]["bindings"]
    ]

def get_tecnicos():
    sparql = """
    PREFIX : <http://www.semanticweb.org/cid34senhas/ontologies/world_cup#>
    SELECT ?nome ?selecao ?ano WHERE {
      ?tecnico a :Coach ;
               :name ?nome ;
               :treinaEquipa ?team .
      ?team :representaPais ?selecao ;
            :participaEmTorneio ?torneio .
      ?torneio :year ?ano .
    }
    """
    results = query_graphdb(sparql)
    if not results: return []
    return [
        {
            "nome": r["nome"]["value"],
            "selecao": r["selecao"]["value"],
            "ano": r["ano"]["value"]
        }
        for r in results["results"]["bindings"]
    ]
    
def get_estadios():
    sparql = """
    PREFIX : <http://www.semanticweb.org/cid34senhas/ontologies/world_cup#>
    SELECT ?nome ?capacidade WHERE {
      ?estadio a :Stadium ;
               :name ?nome ;
               :capacity ?capacidade .
    }
    """
    results = query_graphdb(sparql)
    if not results: return []
    return [
        {
            "nome": r["nome"]["value"],
            "capacidade": r["capacidade"]["value"]
        }
        for r in results["results"]["bindings"]
    ]

def get_gols():
    sparql = """
    PREFIX : <http://www.semanticweb.org/cid34senhas/ontologies/world_cup#>
    SELECT ?jogador_nome ?partida_nome WHERE {
      ?jogador a :Player ;
               :name ?jogador_nome ;
               :marcouGoloEm ?partida_nome .
    }
    """

    results = query_graphdb(sparql)
    if not results: return []
    return [
        {
            "jogador": r["jogador_nome"]["value"],
            "partida": r["partida_nome"]["value"]
        }
        for r in results["results"]["bindings"]
    ]

def get_partidas():
    sparql = """
    PREFIX : <http://www.semanticweb.org/cid34senhas/ontologies/world_cup#>
    SELECT ?nome ?estadio_nome ?data WHERE {
      ?partida a :Match ;
               :name ?nome ;
               :playedAtStadium ?estadio ;
               :matchDate ?data .

      ?estadio :name ?estadio_nome .
    }
    """
    results = query_graphdb(sparql)
    if not results: return []
    return [
        {
            "nome": r["nome"]["value"],
            "estadio": r["estadio_nome"]["value"],
            "data" : r["data"]["value"]
        }
        for r in results["results"]["bindings"]
    ]
def get_torneios():
    sparql = """
    PREFIX : <http://www.semanticweb.org/cid34senhas/ontologies/world_cup#>
    SELECT ?ano ?pais ?vencedor ?nome WHERE {
      ?torneio a :Tournament ;
               :year ?ano ;
               :hostCountry ?pais ;
               :temVencedor ?vencedor ;
               :name ?nome .
    }
    """
    results = query_graphdb(sparql)
    if not results: return []
    return [
        {
            "ano": r["ano"]["value"],
            "pais": r["pais"]["value"].replace("_", " "),
            "vencedor": r["vencedor"]["value"].replace("_", " "),
            "nome": r["nome"]["value"].replace("_", " ")

        }
        for r in results["results"]["bindings"]
    ]

def get_golos_jogador(nome, gols):
    # Conta o número de golos do jogador pelo nome
    return sum(1 for g in gols if g['jogador'] == nome)


@app.route('/pergunta')
def generate_question():
    modo = request.args.get('modo') or session.get('modo')
    temas = request.args.getlist('tema')
    if not modo:
        return redirect(url_for('home'))
    session['modo'] = modo

    # Se vier temas na query, guarda na sessão
    if temas:
        session['temas'] = temas
    else:
        temas = session.get('temas', [])

    if modo == "morte_subita":
        # Inicializa score e flag de vivo
        if 'score' not in session:
            session['score'] = 0
        if 'vivo' not in session:
            session['vivo'] = True
        if not session['vivo']:
            return redirect(url_for('score'))
    else:
        # Inicializa progresso se não existir
        if 'perguntas_respondidas' not in session:
            session['perguntas_respondidas'] = 0
            session['score'] = 0

        # Checa se terminou o quiz
        total_perguntas = MODOS[modo]["total"]
        if session['perguntas_respondidas'] >= total_perguntas:
            return redirect(url_for('score'))

    jogadores = get_jogadores()
    tecnicos = get_tecnicos()
    estadios = get_estadios()
    gols = get_gols()
    partidas = get_partidas()
    torneios = get_torneios()

    if not temas:
        temas = session.get('temas', [])
    # Se não vier nenhum tema, sorteia como antes
    if not temas:
        temas = ['jogador', 'tecnico', 'estadio', 'gol', 'partida', 'matching','pais_mundial', 'jogador_treinador', 'mais_golos', 'vencedor_torneio']

    
    # Limita a 3 temas
    if len(temas) > 3:
        temas = temas[:3]

    # Escolhe aleatoriamente um dos temas selecionados para a pergunta atual
    tema = random.choice(temas)
    if tema == 'pais_mundial':
        # Em que país foi realizado o Mundial de Y?
        if not torneios or len(torneios) < 4:
            return "Erro: Não há torneios suficientes.", 500
        torneios_sample = random.sample(torneios, 4)
        torneio_alvo = random.choice(torneios_sample)
        nome_torneio = torneio_alvo.get('nome', '').lower()
        if 'women' in nome_torneio:
            genero = 'Feminino'
        else:
            genero = 'Masculino'
        pergunta = {
            "tipo": "multipla",
            "texto": f"Em que país foi realizado o Mundial {genero} de {torneio_alvo['ano']}?",
            "opcoes": [t['pais'].split('#')[-1].replace('_', ' ') for t in torneios_sample],
            "resposta": torneio_alvo['pais'].split('#')[-1].replace('_', ' ')
        }
        return render_template('pergunta.html', pergunta=pergunta, temas=temas, modo=modo)

    elif tema == 'jogador_treinador':
        # Qual dos jogadores foi treinador e jogador de uma seleção?
        jogadores_tecnicos = [j['nome'] for j in jogadores if any(t['nome'] == j['nome'] for t in tecnicos)]
        if not jogadores_tecnicos or len(jogadores) < 4:
            return "Erro: Não há jogadores/treinadores suficientes.", 500
        opcoes = random.sample([j['nome'].replace('_', ' ') for j in jogadores], 3)
        resposta = random.choice(jogadores_tecnicos).replace('_', ' ')
        if resposta not in opcoes:
            opcoes.append(resposta)
        random.shuffle(opcoes)
        pergunta = {
            "tipo": "multipla",
            "texto": "Qual dos atletas foi também treinador/a de uma seleção?",
            "opcoes": opcoes,
            "resposta": resposta
        }
        return render_template('pergunta.html', pergunta=pergunta, temas=temas, modo=modo)

    elif tema == 'mais_golos':
        # Entre o jogador x e y quem foi o que marcou mais golos em torneios?
        if len(jogadores) < 2:
            return "Erro: Não há jogadores suficientes.", 500
        jogadores_sample = random.sample(jogadores, 2)
        golos_x = get_golos_jogador(jogadores_sample[0]['nome'], gols)
        golos_y = get_golos_jogador(jogadores_sample[1]['nome'], gols)
        if golos_x > golos_y:
            resposta = jogadores_sample[0]['nome'].replace('_', ' ')
        else:
            resposta = jogadores_sample[1]['nome'].replace('_', ' ')
        pergunta = {
            "tipo": "multipla",
            "texto": f"Entre o jogador {jogadores_sample[0]['nome'].replace('_', ' ')} e {jogadores_sample[1]['nome'].replace('_', ' ')}, quem marcou mais golos em torneios?",
            "opcoes": [jogadores_sample[0]['nome'].replace('_', ' '), jogadores_sample[1]['nome'].replace('_', ' ')],
            "resposta": resposta
        }
        return render_template('pergunta.html', pergunta=pergunta, temas=temas, modo=modo)
    
    elif tema == 'vencedor_torneio':
        # Quem foi o vencedor do torneio x?
        if not torneios or len(torneios) < 4:
            return "Erro: Não há torneios suficientes.", 500
        torneios_sample = random.sample(torneios, 4)
        torneio_alvo = random.choice(torneios_sample)

        # Detecta o género pelo nome do torneio
        nome_torneio = torneio_alvo.get('nome', '').lower()
        if 'women' in nome_torneio:
            genero = 'Feminino'
        else:
            genero = 'Masculino'

        pergunta = {
            "tipo": "multipla",
            "texto": f"Quem foi a equipa vencedora do Mundial {genero} de {torneio_alvo['ano']}?",
            "opcoes": [
                re.sub(
                    r'\s(woman|man)\sWC\s\d{4}$', '', 
                    t['vencedor'].split('#')[-1] if '#' in t['vencedor'] else t['vencedor']
                ).replace('_', ' ')
                for t in torneios_sample
            ],
            "resposta": re.sub(
                r'\s(woman|man)\sWC\s\d{4}$', '', 
                torneio_alvo['vencedor'].split('#')[-1] if '#' in torneio_alvo['vencedor'] else torneio_alvo['vencedor']
            ).replace('_', ' ')
        }
        return render_template('pergunta.html', pergunta=pergunta)


    elif tema == 'jogador':
        if not jogadores or len(jogadores) < 4:
            return "Erro: Não há jogadores suficientes na base de dados.", 500
        
        
        jogadores_sample = random.sample(jogadores, 4)
        jogador_alvo = random.choice(jogadores_sample)
        pergunta = {
            "tipo": "multipla",
            "texto": f"Quando nasceu o/a jogador/a {jogador_alvo['nome'].replace('_',' ')}?",
            "opcoes": [j['nascimento'] for j in jogadores_sample],
            "resposta": jogador_alvo['nascimento']
        }
        return render_template('pergunta.html', pergunta=pergunta, temas=temas, modo=modo)

    elif tema == 'tecnico':
        if not tecnicos or len(tecnicos) < 4:
            return "Erro: Não há técnicos suficientes na base de dados.", 500
        tecnicos_sample = random.sample(tecnicos, 4)
        tecnico_alvo = random.choice(tecnicos_sample)
        # Detecta se é seleção masculina ou feminina de forma robusta
        selecao_nome = tecnico_alvo['selecao']
        ano = str(tecnico_alvo['ano'])
    
        if f'_man_WC_{ano}' in selecao_nome:
            genero = 'masculina'
            pais = selecao_nome.split(f'_man_WC_{ano}')[0]
        elif f'_woman_WC_{ano}' in selecao_nome:
            genero = 'feminina'
            pais = selecao_nome.split(f'_woman_WC_{ano}')[0]
        else:
            genero = ''
            pais = selecao_nome
    
        pais = pais.replace("http://www.semanticweb.org/cid34senhas/ontologies/world_cup#", "").replace("_", " ")
    
        if genero:
            texto_pergunta = f"Que treinador treinou a seleção {genero} de {pais} no Mundial de {ano}?"
        else:
            texto_pergunta = f"Que treinador treinou {pais} no Mundial de {ano}?"
    
        pergunta = {
            "tipo": "multipla",
            "texto": texto_pergunta,
            "opcoes": [t['nome'].replace("_", " ") for t in tecnicos_sample],
            "resposta": tecnico_alvo['nome'].replace("_", " ")
        }
        return render_template('pergunta.html', pergunta=pergunta, temas=temas, modo=modo)

    elif tema == 'estadio':
        if not estadios or len(estadios) < 4:
            return "Erro: Não há estádios suficientes na base de dados.", 500
        estadios_sample = random.sample(estadios, 4)
        estadio_alvo = random.choice(estadios_sample)
        pergunta = {
            "tipo": "multipla",
            "texto": f"Qual a capacidade do estádio {estadio_alvo['nome'].replace('_',' ')}?",
            "opcoes": [e['capacidade'] for e in estadios_sample],
            "resposta": estadio_alvo['capacidade']
        }
        return render_template('pergunta.html', pergunta=pergunta, temas=temas, modo=modo)

    elif tema == 'gol':
        if not gols or len(gols) < 4 or not jogadores or len(jogadores) < 2:
            return "Erro: Não há gols ou jogadores suficientes na base de dados.", 500
        gols_sample = random.sample(gols, 4)
        gol_alvo = random.choice(gols_sample)
        jogador_falso = random.choice([g for g in jogadores if g['nome'] != gol_alvo['jogador']])
        opcoes = [gol_alvo['jogador'], jogador_falso['nome']]
        random.shuffle(opcoes)
        partida_str = gol_alvo['partida'].replace("http://www.semanticweb.org/cid34senhas/ontologies/world_cup#", "").replace("_", " ")
        partida_name = re.split(r' [MW] \d{4} \d+', partida_str)[0].strip()
        match = re.search(r'[WM] (\d{4})', partida_str)
        print(partida_str)
        ano = match.group(1) if match else ""
        pergunta = {
            "tipo": "vf",
            "texto": f"O jogador {opcoes[0].replace('_',' ')} marcou golo na partida de {partida_name} em {ano}?",
            "resposta": "Verdadeiro" if opcoes[0] == gol_alvo['jogador'] else "Falso"
        }
        return render_template('pergunta.html', pergunta=pergunta, temas=temas, modo=modo)

    elif tema == 'partida':
        if not partidas or len(partidas) < 4:
            return "Erro: Não há partidas suficientes na base de dados.", 500
        partidas_sample = random.sample(partidas, 4)
        partida_alvo = random.choice(partidas_sample)
        pergunta = {
            "tipo": "multipla",
            "texto": f"Onde foi jogada a partida {partida_alvo['nome'].replace('_',' ')} no dia {partida_alvo['data']}?",
            "opcoes": [p['estadio'].replace("_"," ") for p in partidas_sample],
            "resposta": partida_alvo['estadio'].replace("_"," ")
        }
        return render_template('pergunta.html', pergunta=pergunta, temas=temas, modo=modo)

    elif tema == 'matching':
        if not jogadores or len(jogadores) < 4:
            return "Erro: Não há jogadores suficientes para matching.", 500
        jogadores_sample = random.sample(jogadores, 4)
        pares = {j['nome'].replace('_',' '): j['posicao'].split('/')[0].strip() for j in jogadores_sample}
        opcoes = list(set(pares.values()))
        posicoes_padrao = ['goalkeeper', 'defender', 'midfielder', 'forward']
        for pos in posicoes_padrao:
            if pos not in opcoes and len(opcoes) < 4:
                opcoes.append(pos)
        opcoes = random.sample(opcoes, 4)
        pergunta = {
            "tipo": "matching",
            "texto": "Associe cada atleta à sua posição",
            "itens": list(pares.keys()),
            "opcoes": opcoes,
            "respostas": list(pares.values())
        }
        return render_template('matching.html', pergunta=pergunta, temas=temas, modo=modo)

# O resto do teu código (check_answer, reiniciar, etc.) pode ficar igual.

@app.route('/resposta', methods=['POST'])
def check_answer():
    modo = session.get('modo')
    temas = request.form.getlist('tema')  # Recupera os temas enviados pelo formulário

    if modo == "morte_subita":
        resposta_usuario = request.form.get('resposta')
        resposta_correta = request.form.get('resposta_correta')
        tipo_pergunta = request.form.get('tipo_pergunta')
        correta = resposta_usuario == resposta_correta
        if correta:
            session['score'] = session.get('score', 0) + 1
            # Redireciona para a próxima pergunta mantendo modo e temas
            return redirect(url_for('generate_question', modo=modo, **{'tema': temas}))
        else:
            session['vivo'] = False
            # Atualiza maior score se necessário
            maior_score = session.get('maior_score', 0)
            if session['score'] > maior_score:
                session['maior_score'] = session['score']
            return redirect(url_for('score'))
    else:
        resposta_usuario = request.form.get('resposta')
        resposta_correta = request.form.get('resposta_correta')
        tipo_pergunta = request.form.get('tipo_pergunta')

        # Incrementa o número de perguntas respondidas
        session['perguntas_respondidas'] = session.get('perguntas_respondidas', 0) + 1

        # Verificar se a resposta está correta
        if tipo_pergunta == 'matching':
            itens = request.form.getlist('item')
            respostas_corretas = request.form.getlist('resposta_correta')
            respostas = []
            for idx in range(len(itens)):
                respostas.append(request.form.get(f'resposta_{idx}'))
            acertos = sum([r == c for r, c in zip(respostas, respostas_corretas)])
            session['score'] = session.get('score', 0) + acertos
            return render_template('respostas_matching.html',
                                  acertos=acertos,
                                  total=len(itens),
                                  score=session['score'],
                                  temas=temas,
                                  modo=modo)
        else:
            correta = resposta_usuario == resposta_correta
            if correta:
                session['score'] = session.get('score', 0) + 1
            # Mostra sempre a página de resposta, mesmo se errar
            return render_template('resposta.html', 
                      correta=correta, 
                      resposta_correta=resposta_correta,
                      score=session['score'],
                      temas=temas,
                      modo=modo)


@app.route('/score')
def score():
    modo = session.get('modo')
    score = session.get('score', 0)
    perguntas_respondidas = session.get('perguntas_respondidas', 0)
    if not modo:
        return redirect(url_for('home'))
    nome_modo = MODOS[modo]["nome"]

    # Corrige aqui: garante que maior_score existe sempre
    maior_score = session.get('maior_score', 0)

    if modo == "morte_subita":
        passou = False
        min_acertos = 0
        total = score
    else:
        min_acertos = MODOS[modo]["min_acertos"]
        total = MODOS[modo]["total"]
        passou = score >= min_acertos

        # Salva o modo concluído com sucesso
        if passou:
            if 'modos_concluidos' not in session:
                session['modos_concluidos'] = []
            if modo not in session['modos_concluidos']:
                session['modos_concluidos'].append(modo)
                session.modified = True

    # Usa maior_score aqui sem erro
    if score > maior_score:
        session['maior_score'] = score

    return render_template('score.html', passou=passou, score=score, total=total, min_acertos=min_acertos, nome_modo=nome_modo)


@app.route('/reiniciar')
def reiniciar():
    modos_concluidos = session.get('modos_concluidos', [])
    session.clear()
    session['modos_concluidos'] = modos_concluidos
    return redirect(url_for('home'))


@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True, port=5001)