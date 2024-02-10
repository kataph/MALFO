import rdflib as rl 
import uuid
import hashlib
import os
import datetime
import functools

from bs4 import BeautifulSoup
from rdflib.namespace import OWL, RDF, RDFS



ROOT_URL = "https://www.example.com/"
MALFO_URL = "https://www.w3id.org/MALFO#"
INPUT_GRAPHML = input("Input the graphml file name or path (with the extension). The file must follow the convention hardcoded in this script. ")
OUTPUT_TURTLE = 'graphml2rdf-out.ttl'

# change this map to change the conventional meaning of colors
COLORS2CATEGORIES = [
("#ffcc00", "FunctionCompatible"),
("#ff0000", "Malfunction"),
]

# change this map to change the conventional meaning of shapes
SHAPES2CATEGORIES = [
("roundrectangle", "State"),
("rectangle", "Process"),
("hexagon", "Event"),
("com.yworks.entityRelationship.big_entity", "Occurrent"),
]

# change this map to map abbreviation to MALFO owl terms
ABBREVIATIONS = [
    ("facilitative", "facilPreconditionFor"),
    ("preventive", "prevPreconditionFor"),
    ("physical", "hasPhysicalConseq"),
]

def adjust_abbreviations(string: str) -> str:
    for (short, complete) in ABBREVIATIONS:
        string = string.replace(short, complete)
    return string

def mapTemplate(input: str, input_name: str, map: list[tuple]):
    for pair in map:
        if input.lower() == pair[0].lower():
            return pair[1]
    print(f"Attention: unknown {input_name}: {input}.")

colors2categories = functools.partial(mapTemplate, input_name = "color", map = COLORS2CATEGORIES)
shapes2categories = functools.partial(mapTemplate, input_name = "shapes", map = SHAPES2CATEGORIES)

def format(string):
    return string.replace("\n", " ")


base = rl.Namespace(ROOT_URL)
MALFO = rl.Namespace(MALFO_URL)

soup = BeautifulSoup(open(INPUT_GRAPHML), features="xml")
edges = soup.findAll("edge")

g = rl.Graph()
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)
g.bind("MALFO", MALFO)


for edge in edges:
    if not edge.find("y:EdgeLabel"):
        continue

    source = soup.find("node", id=edge.get("source"))
    target = soup.find("node", id=edge.get("target"))

    if not source.find("y:Fill") or not target.find("y:Fill"):
        continue
    if not source.find("y:Fill").get("color") or not target.find("y:Fill").get("color"):
        continue
    
    label_e_str = " ".join([EdgeLabel.getText().replace("\n","") for EdgeLabel in edge.findAll("EdgeLabel")]).strip()
    label_e = rl.Literal(format(adjust_abbreviations(label_e_str)))
    color_e = edge.find("y:LineStyle").get("color")

    label_s = rl.Literal(format(source.find("y:NodeLabel").getText()))
    color_s = source.find("y:Fill").get("color")
    shape_s = source.find("y:Shape").get("type")

    label_t = rl.Literal(format(target.find("y:NodeLabel").getText()))
    color_t = target.find("y:Fill").get("color")
    shape_t = target.find("y:Shape").get("type")

    category_s = MALFO[shapes2categories(shape_s)]
    function_s = MALFO[colors2categories(color_s)]
    category_t = MALFO[shapes2categories(shape_t)]
    function_t = MALFO[colors2categories(color_t)]
    category_e = MALFO[label_e]

    if any(x == MALFO[None] for x in [category_s, function_s, category_t, function_t, category_e]):
        print("Some node lacks some required property: skipping...")
        continue

    occurrent_s = base[hashlib.sha256(label_s.encode('utf-8')).hexdigest()]#base[str(uuid.uuid4())]
    occurrent_t = base[hashlib.sha256(label_t.encode('utf-8')).hexdigest()]#base[str(uuid.uuid4())]
    
    g.add((category_s, RDF.type, OWL.Class))
    g.add((category_t, RDF.type, OWL.Class))
    g.add((category_e, RDF.type, OWL.ObjectProperty))

    g.add((occurrent_s, RDF.type, category_s))
    g.add((occurrent_s, RDF.type, function_s))
    g.add((occurrent_s, RDFS.label, label_s))
    g.add((occurrent_t, RDF.type, category_t))
    g.add((occurrent_t, RDF.type, function_t))
    g.add((occurrent_t, RDFS.label, label_t))
    g.add((occurrent_s, category_e, occurrent_t))
    g.add((category_e, RDF.type, OWL.ObjectProperty))

document = rl.BNode()
g.add((document, RDF.type, OWL.Ontology))
g.add((document, RDFS.comment, rl.Literal(f'Graph automatically built from \'{INPUT_GRAPHML}\' on {str(datetime.datetime.now())}')))
g.add((document, OWL.imports, rl.URIRef('https://www.w3id.org/MALFO')))


g.serialize(OUTPUT_TURTLE, format = "ttl")   

