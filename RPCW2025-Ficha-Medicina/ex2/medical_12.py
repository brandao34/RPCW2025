from rdflib import Graph, Namespace, Literal


g = Graph()
g.parse("med_doentes.ttl")

#Cria uma query CONSTRUCT que diagnostique a doença de cada pessoa, ou seja, produza uma lista
#de triplos com a forma :patientX :hasDisease :diseaseY. No fim, acrescenta estes triplos à
#ontologia;
#
#
#
q = """
CONSTRUCT {
    ?p :hasDisease ?d .
}
WHERE {
    { ?p :exhibitsSymptom ?s . }
    { ?p :exhibitsSymptom ?a . }
    { ?p :exhibitsSymptom ?l . }
    { ?d :hasSymptom ?s . }
    { ?d :hasSymptom ?a . }
    { ?d :hasSymptom ?l . }
}

""" 

n = Namespace("http://www.example.org/disease-ontology#")


for r in g.query(q):
    print(r[0], "hasDisease", r[2])
    #g.add((r[0], n.hasDisease, r[2]))


