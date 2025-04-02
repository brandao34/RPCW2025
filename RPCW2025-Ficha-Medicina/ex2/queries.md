# 2.11 

## Quantas doenças estão presentes na ontologia?

``` 
prefix : <http://www.example.org/disease-ontology#>

SELECT (COUNT(DISTINCT ?class) AS ?count) WHERE {
  ?class a :Disease .
}

```
R:43 

## Que doenças estão associadas ao sintoma "yellowish_skin"? 

``` 
prefix : <http://www.example.org/disease-ontology#>
prefix owl: <http://www.w3.org/2002/07/owl#>

SELECT ?Doenca WHERE {
  ?Doenca :hasSymptom :yellowish_skin .
}

```

R:
:Alcoholic_hepatitis	
:Chronic_cholestasis	
:Hepatitis_B	
:Hepatitis_C	
:Hepatitis_D	
:Hepatitis_E	
:Jaundice	
:hepatitis_A

## Que doenças estão associadas ao tratamento "exercise"?

``` 
prefix : <http://www.example.org/disease-ontology#>
prefix owl: <http://www.w3.org/2002/07/owl#>

SELECT ?Doenca WHERE {
  ?Doenca :hasTreatment :Exercise .
}


``` 
R:
:Diabetes


## Produz uma lista ordenada alfabeticamente com o nome dos doentes ? 


``` 
PREFIX : <http://www.example.org/disease-ontology#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT  ?nome
WHERE {
  ?doente a :Patient ;
          :name ?nome .
}
ORDER BY ?nome

````
R: 10002 Resultados 

Aadeep Ascencoo^^xsd:string	
Aadhira Bem-Haja^^xsd:string	
Aadvik Grifo^^xsd:string	
Aafiya Acafroo^^xsd:string	
Aahan Palancha^^xsd:string	
Aahana Rogeiro^^xsd:string	
Aaish Barriga^^xsd:string	
Aakarshan Potencio^^xsd:string	
Aakarshan Serradio^^xsd:string	
Aaliyah Fial^^xsd:string	
Aamna Baracal^^xsd:string	
Aankit Malhadeiro^^xsd:string	
Aaradhya Fradigano^^xsd:string	
Aarayna Tecedeiro^^xsd:string	
Aaron Balonas^^xsd:string