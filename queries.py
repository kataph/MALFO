CLASSIFICATION_QUERIES = {
"rank1": [],
"rank2": [
"""
##[reduced to RANK1]
## SELECTS all malfunction-processes # Complete knowledge about functional compatibility of putative malfunction-processes is assumed (for the FILTER NOT EXISTS, otherwise some non-malfunction-processes may be returned)
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX malfo: <https://www.w3id.org/MALFO#>
INSERT {?x a malfo:MalfunctionProcess}
WHERE {
	?x a malfo:Process .
	?x a malfo:Malfunction .
}""",
"""
##[reduced to RANK1]
## SELECTS all faults # Complete knowledge about functional compatibility of putative faults is assumed (for the FILTER NOT EXISTS, otherwise some non-faults may be returned)
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX malfo: <https://www.w3id.org/MALFO#>
INSERT {?x a malfo:Fault}
WHERE {
	?x a malfo:State .
	?x a malfo:Malfunction .
	?z malfo:internalTo ?x . 
	?z malfo:achieves ?x .
}"""],
"rank3": 
["""##[reduced to RANK2]
## SELECTS all failures # Complete knowledge about functional compatibility of putative failures is assumed (for the FILTER NOT EXISTS, otherwise some non-failures may be returned)
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX malfo: <https://www.w3id.org/MALFO#>
INSERT {?x a malfo:Failure}
WHERE {
	?x a malfo:Event .
	?x a malfo:Malfunction .
	?x malfo:achieves ?y . ?y a malfo:Fault .
}""",

"""##[reduced to RANK2]; requires negation-as-failure
## SELECTS all down-states # Complete knowledge about functional compatibility of putative down-states  is assumed (for the FILTER NOT EXISTS, otherwise some non-down-states  may be returned)
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX malfo: <https://www.w3id.org/MALFO#>
INSERT {?x a malfo:DownState}
WHERE {
	?x a malfo:State .
	?x a malfo:Malfunction .
	FILTER NOT EXISTS {?x a malfo:Fault .}
}"""],
"rank4":
["""##[reduced to RANK3]
## SELECTS all failure conditions
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX malfo: <https://www.w3id.org/MALFO#>
INSERT {?x rdf:type malfo:FailureCondition} 
WHERE {
	?x a malfo:State .
	?fa a malfo:Failure .
	{?x (malfo:achieves|malfo:allows|malfo:facilPreconditionFor|malfo:hasPhysicalConseq)* ?fa .} 
	UNION
	{?x malfo:prevPreconditionFor ?st .
	?st malfo:disallows ?fa .} 
	FILTER NOT EXISTS {?x a malfo:Malfunction}
}""",
"""##[reduced to RANK3]
## SELECTS all failure mechanisms
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX malfo: <https://www.w3id.org/MALFO#>
INSERT {?x a malfo:FailureMechanism}
WHERE {
	?x (malfo:achieves|malfo:allows|malfo:facilPreconditionFor|malfo:hasPhysicalConseq)* ?fa . ?fa a malfo:Failure .
	{?x a malfo:Process} 
	UNION
	{?x a malfo:Event} 
	FILTER NOT EXISTS {?x a malfo:Malfunction}
}""",
"""##[reduced to RANK3]; requires negation-as-failure
## SELECTS all non-performance event # Complete knowledge about functional compatibility of putative non-performance event is assumed (for the FILTER NOT EXISTS, otherwise some non-non-performance-event  may be returned)
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX malfo: <https://www.w3id.org/MALFO#>
INSERT {?x a malfo:NonPerformanceEvent}	
WHERE {
	?x a malfo:Event .
	?x a malfo:Malfunction .
	FILTER NOT EXISTS {?x malfo:achieves ?y . ?y a malfo:Fault .}
	FILTER NOT EXISTS {?x a malfo:Failure}
}""",
"""##[reduced to RANK3]; requires negation-as-failure
## SELECTS all mere symptoms # Complete knowledge about causal consequences of putative mere sympoms is assumed (for the FILTER NOT EXISTS, otherwise some non-mere-symptoms may be returned)
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX malfo: <https://www.w3id.org/MALFO#>
INSERT {?x a malfo:MereSymptom}
WHERE {
	?mal (malfo:achieves|malfo:allows|malfo:prevents|malfo:disallows) ?x . ?mal a malfo:Malfunction
	FILTER NOT EXISTS {?x a malfo:FailureMechanism}
	FILTER NOT EXISTS {?x a malfo:FailureCondition}
	FILTER NOT EXISTS {?x a malfo:Malfunction}
}"""]
}

CAUSATION_RULES = {
    "rank1":[
        """## hasPhysicalConseq is the neutral element for causation
		PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
		PREFIX malfo: <https://www.w3id.org/MALFO#>
		INSERT {?x ?p ?y}
        WHERE {
			?x malfo:hasPhysicalConseq* ?x1 . ?x1 ?p ?x2 . ?x2 malfo:hasPhysicalConseq* ?y . 
            VALUES ?p {malfo:achieves malfo:allows malfo:disallows malfo:prevents malfo:facilPreconditionFor malfo:prevPreconditionFor}
		}""",],
    "rank2":[
        """## APPLIES THE DEFINITION OF allows; requires negation-as-failure
		PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
		PREFIX malfo: <https://www.w3id.org/MALFO#>
		INSERT {?x malfo:allows ?y}
        WHERE {
			{?x malfo:achieves|malfo:maintains ?z .
            ?z malfo:facilPreconditionFor ?y}
            UNION
            {?x malfo:prevents ?z .
            ?z malfo:prevPreconditionFor ?y .
            FILTER NOT EXISTS {?w rdf:type malfo:State . ?x malfo:achieves ?w . ?w malfo:prevPreconditionFor ?y}
            }
		}""",
        """## APPLIES THE DEFINITION OF disallows
		PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
		PREFIX malfo: <https://www.w3id.org/MALFO#>
		INSERT {?x malfo:disallows ?y}
        WHERE {
			{?x malfo:achieves|malfo:maintains ?z .
            ?z malfo:prevPreconditionFor ?y}
            UNION
            {?x malfo:prevents ?z .
            ?z malfo:facilPreconditionFor ?y}
		}""",
        """## APPLIES THE DEFINITION OF prevents
		PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
		PREFIX malfo: <https://www.w3id.org/MALFO#>
		INSERT {?x malfo:prevents ?y}
        WHERE {
			?x malfo:achieves ?z .
            ?z malfo:incompatibleWith ?y
		}""",
	]
}

RANGE_DOMAIN_CONSTRAINTS = {
    "achieves":"""
	## check violations of range domain axioms of achieves:
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX malfo: <https://www.w3id.org/MALFO#>
    ASK {
        {?occ malfo:achieves ?ev . ?ev rdf:type malfo:Event} 
        UNION 
        {?st malfo:achieves ?proc . ?st rdf:type malfo:State . ?proc rdf:type malfo:Process} 
        }
	""",
    "prevents":"""
	## check violations of range domain axioms of prevents:
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX malfo: <https://www.w3id.org/MALFO#>
    ASK {
        {?occ malfo:prevents ?ev . ?ev rdf:type malfo:Event} 
        UNION 
        {?st malfo:prevents ?proc . ?st rdf:type malfo:State . ?proc rdf:type malfo:Process} 
        }
	""",
    "allows":"""
	## check violations of range domain axioms of allows:
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX malfo: <https://www.w3id.org/MALFO#>
    ASK {
        {?st malfo:allows ?occ . ?st rdf:type malfo:State} 
        }
	""",
    "disallows":"""
	## check violations of range domain axioms of disallows:
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX malfo: <https://www.w3id.org/MALFO#>
    ASK {
        {?st malfo:disallows ?occ . ?st rdf:type malfo:State} 
        }
	"""
}

SELECT_FINER_CAUSES = {
    "absolute": """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX malfo: <https://www.w3id.org/MALFO#>
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	SELECT DISTINCT ?x ?p ?y
	WHERE {
		?x (malfo:achieves|malfo:allows|malfo:facilPreconditionFor|malfo:hasPhysicalConseq) ?fau . ?fau a malfo:Fault .
		?fau (malfo:achieves|malfo:allows|malfo:facilPreconditionFor|malfo:hasPhysicalConseq)+ ?y . #?y a malfo:Fault .
		FILTER NOT EXISTS {?fau2 a malfo:Fault . 
				?fau (malfo:achieves|malfo:allows|malfo:facilPreconditionFor|malfo:hasPhysicalConseq)+ ?fau2 . 
				?fau2 (malfo:achieves|malfo:allows|malfo:facilPreconditionFor|malfo:hasPhysicalConseq)+ ?y}
        BIND(malfo:absoluteCauseOf as ?p)
	}""",
    "ultimate":""""""
}
