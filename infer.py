import rdflib as rl
from time import time
from queries import CLASSIFICATION_QUERIES, CAUSATION_RULES, RANGE_DOMAIN_CONSTRAINTS

INPUT_GRAPH = input("Input the name or path of the graph on which apply ad-hoc reasoning: ")
# INPUT_GRAPH = "graphml2rdf-out.ttl"
g = rl.Graph()
g.parse(INPUT_GRAPH)

for rank, queries in CAUSATION_RULES.items():
    for query_index, query in enumerate(queries):
        print(f'Executing {query_index}-th causation rule query in {rank}...')
        print(f'Query: {query}')  
        start = time()
        g.update(query)
        end = time()
        print(f'... execution took {end - start} seconds.')

for rank, queries in CLASSIFICATION_QUERIES.items():
    for query_index, query in enumerate(queries):
        print(f'Executing {query_index}-th classification query in {rank}...')
        print(f'Query: {query}')  
        start = time()
        g.update(query)
        end = time()
        print(f'... execution took {end - start} seconds.')

violations = []     
for key, query in RANGE_DOMAIN_CONSTRAINTS.items():
    print(f'Executing range domain check query for {key}...')
    print(f'Query: {query}') 
    start = time()
    violation = g.query(query)
    violations.append(violation)
    if violation:
        print(f'The graph is not compliant with the ontology: domain/range axioms for {key} are violated.')
    end = time()
    print(f'... execution took {end - start} seconds.')

if any(violations):
    print("The graph is not compliant with the ontology: some domain/range axioms are violated, check logs.")
else:
    print("No domain/range axioms are violated.")

g.update("""
         PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
         PREFIX owl:<http://www.w3.org/2002/07/owl#>
         INSERT {?o rdfs:comment 'Graph enriched with the inferences from the script -MALFO_insert_queries.py-'} 
         WHERE {?o a owl:Ontology}
         """)
g.serialize(INPUT_GRAPH[:-4] + "_inferences.ttl", format="ttl")
