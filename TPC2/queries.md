# 1 - Quantos triplos existem na Ontologia?

```
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
select * where {
    ?s ?o ?p
}
```
6603

# 2 - Que classes estão definidas?


``` 
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT DISTINCT ?class WHERE {
   ?class a owl:Class 

}
``` 

Estao definidas 102 classes 



# 3 - Que propriedades tem a classe "Rei"?

``` 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>

SELECT distinct ?prop WHERE {
  ?s a :Rei .
  ?s ?prop ?o .
} order by ?prop


```

1
:ascendente
2
:casa
3
:cognomes
4
:descendente
5
:enterro
6
:localNascimento
7
:morte
8
:nascimento
9
:nome
10
:notas
11
:posicao
12
:predecessor
13
:sucessor
14
:temReinado
15
rdf:type




# 4 - Quantos reis aparecem na ontologia?

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>

SELECT (count(distinct ?rei) as ?count) WHERE {
  ?rei a :Rei .
  
} 

```

R: 32 
# 5 - Calcula uma tabela com o seu nome, data de nascimento e cognome.

``` 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>

SELECT  ?nome ?nascimento ?cognome  WHERE {
  ?rei a :Rei .
 ?rei :nome ?nome .
  ?rei :nascimento ?nascimento .
  ?rei :cognomes ?cognome .
    
} 



``` 
R: 34 entradas 

| nome        | nascimento           | cognome |
|------------|----------------------|------------------------------------------------|
| "D. Manuel I" | "31 de maio de 1469" | "O Venturoso, O Bem-Aventurado, O Pomposo" |
| "D. João I" | "11 de abril de 1357" | "O da Boa Memória" |
| "D. Pedro I" | "8 de abril de 1320" | "O Justiceiro, O Cruel, O Cru, O Vingativo, O Tartamudo, O Até-ao-Fim-do-Mundo-Apaixonado" |





# 6 - Acrescenta à tabela anterior a dinastia em que cada rei reinou.

``` 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>

SELECT  ?nome ?nascimento ?cognome ?distania WHERE {
  ?rei a :Rei .
 ?rei :nome ?nome .
  ?rei :nascimento ?nascimento .
  ?rei :cognomes ?cognome .
  ?rei :temReinado ?reinado . 
  ?reinado :dinastia ?temDisnastia . 
  ?temDisnastia :nome ?distania .
} 

``` 
R: 34 entradas

| nome        | nascimento           | cognome | Dinastia | 
|------------|----------------------|------------------------------------------------|-----------------------------| 
| "D. Manuel I" | "31 de maio de 1469" | "O Venturoso, O Bem-Aventurado, O Pomposo" | "Dinastia de Avis / Dinastia Joanina" |
| "D. João I" | "11 de abril de 1357" | "O da Boa Memória" | "Dinastia de Avis / Dinastia Joanina" |
| "D. Pedro I" | "8 de abril de 1320" | "O Justiceiro, O Cruel, O Cru, O Vingativo, O Tartamudo, O Até-ao-Fim-do-Mundo-Apaixonado" | "Dinastia de Borgonha / Dinastia Afonsina" |

# 7 - Qual a distribuição de reis pelas 4 dinastias?

``` 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>

SELECT (count(distinct ?rei) as ?count) ?distania WHERE {
  ?rei a :Rei .
 ?rei :nome ?nome .
  ?rei :nascimento ?nascimento .
  ?rei :cognomes ?cognome .
  ?rei :temReinado ?reinado . 
  ?reinado :dinastia ?temDisnastia . 
  ?temDisnastia :nome ?distania .
} group by ?distania

``` 


| count          | dinastia                                      |
|---------------|---------------------------------------------|
| "8"  | "Dinastia de Avis / Dinastia Joanina"      |
| "9"  | "Dinastia de Borgonha / Dinastia Afonsina" |
| "3"  | "Dinastia Filipina"                       |
| "12" | "Dinastia de Bragança / Dinastia Brigantina" |



# 8 - Lista os descobrimentos (sua descrição) por ordem cronológica.

``` 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>

SELECT distinct ?descricao WHERE {
  ?s a :Descobrimento .
  ?s :data ?data .
  ?s :notas ?descricao
} order by ?data

```
R: 82 entradas 

ex: 
|Data | Descricao| 
|---------|----------| 
|"1336" | "Provável primeira expedição às ilhas Canárias, a que se seguiram expedições adicionais em 1340 e 1341, embora tal seja disputado."| 



# 9 - Lista as várias conquistas, nome e data, com o nome do rei que reinava no momento.

``` 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>


Select distinct ?conquista ?data ?reinado Where { 
 ?s a :Conquista .
 ?s :nome ?conquista.
 ?s :data ?data .
 ?s :temReinado ?temReinado .
 ?temReinado :temMonarca ?rei .
 ?rei :nome ?reinado . 
}

``` 
R:18 entradas 

| conquista                          | data  | reinado       |
|------------------------------------|------|--------------|
| "Conquista de Beja"               | "1159" | "D. Afonso I" |
| "Conquista do Castelo de Cera"    | "1159" | "D. Afonso I" |
| "Reconquista de Beja"             | "1162" | "D. Afonso I" |
| "Conquista"                        | "1158" | "D. Afonso I" |


# 10 - Calcula uma tabela com o nome, data de nascimento e número de mandatos de todos os presidentes portugueses.


``` 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>

SELECT distinct  ?nome ?nascimento (count(distinct ?mandatos) as ?count) WHERE {
  ?s a :Presidente .
  ?s :nome ?nome .
  ?s :nascimento ?nascimento . 
  ?s :mandato ?mandatos
} group by ?nascimento ?nome
``` 

R: 17 Entradas 


| #  | Nome                                    | Nascimento              | Count |
|----|-----------------------------------------|-------------------------|-------|
| 1  | José Mendes Cabeçadas Júnior           | 19 de setembro de 1883  | 1     |
| 2  | António Óscar de Fragoso Carmona       | 24 de novembro de 1869  | 4     |
| 3  | António de Oliveira Salazar            | 28 de abril de 1889     | 1     |
| 4  | Francisco Higino Craveiro Lopes        | 12 de abril de 1894     | 1     |




# 11 - Quantos mandatos teve o presidente Sidónio Pais? Em que datas iniciaram e terminaram esses mndatos?

``` 
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX ex: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>

SELECT ?nome (COUNT(?mandato) AS ?total) ?começo ?fim WHERE {
  ?p a ex:Presidente .
  ?p :nome ?nome .
  ?p :mandato ?mandato .
  ?mandato :comeco ?começo .
  ?mandato :fim ?fim .
	
  FILTER(REGEX(?nome, "^Sidónio( [A-Z][a-z]*)* Pais$", "i"))
}
GROUP BY ?nome ?começo ?fim

``` 

# 12 - Quais os nomes dos partidos politicos presentes na ontologia?
``` 


PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX ex: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>

SELECT ?partido WHERE {
  ?p a ex:Partido .
  ?p :nome ?partido .
}
GROUP BY ?partido
``` 


# 13 - Qual a distribuição dos militantes por cada partido politico?
``` 


PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX ex: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>

SELECT  ?nome (COUNT(?militante) AS ?total) WHERE {
  ?p a ex:Partido .
  ?p :temMilitante ?militante .
  ?p :nome ?nome
}
GROUP BY ?nome
``` 



# 14 - Qual o partido com maior número de presidentes militantes?
``` 


PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX ex: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>

SELECT ?nome (COUNT(?militante) AS ?total) WHERE {
  ?p a ex:Partido .
  ?p :temMilitante ?militante .
  ?p :nome ?nome
}
GROUP BY ?nome
ORDER BY DESC(?total)
LIMIT 1
``` 
