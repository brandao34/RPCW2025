## Query 1: 

```
SELECT (COUNT(DISTINCT ?class) AS ?count) WHERE {
  ?class a owl:Class .
}
```

R: 12  ( mas devia ser 10 )


## Query 2: 

```
SELECT (COUNT(DISTINCT ?class) AS ?count) WHERE {
  ?class a owl:ObjectProperty .
}
```

R: 11 


## Query 3: 

```
SELECT (COUNT(DISTINCT ?class) AS ?count) WHERE {
  ?class a owl:NamedIndividual .
}
```

R: 17 

## Query 4: 


PREFIX : <http://www.semanticweb.org/cid34senhas/ontologies/2025/Historia_inferida#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?agricultor WHERE {
  ?agricultor :Cultiva :Tomate .
}

R: Carlos 


## Query 5 


PREFIX : <http://www.semanticweb.org/cid34senhas/ontologies/2025/Historia_inferida#>
PREFIX historia: <http://www.semanticweb.org/cid34senhas/ontologies/2025/historia#>

SELECT DISTINCT ?empregador WHERE {
  ?trabalhador a :Trabalhador_Temp. 
  ?empregrador :temTrabalhador ?empregador. 
               
}

R: Joao 
