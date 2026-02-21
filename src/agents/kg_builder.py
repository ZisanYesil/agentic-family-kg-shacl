from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef
from rdflib.namespace import XSD
import os

FHKB = Namespace("http://www.example.com/genealogy.owl#")


def _to_uri(name: str) -> URIRef:
    # Turn "John Doe" -> fhkb:john_doe
    safe = name.strip().lower().replace(" ", "_")
    return FHKB[safe]


def build_kg(iteration, issues, extracted_facts, output_dir="runs"):
    """
    Builds a knowledge graph from extracted facts.
    Iteration 1 is naive.
    Later iterations apply fix rules based on SHACL feedback (issues).
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/iteration_{iteration}.ttl"

    g = Graph()
    g.bind("fhkb", FHKB)
    g.bind("rdfs", RDFS)

    #1) naive build from facts
    for person_name, facts in extracted_facts.items():
        person_uri = _to_uri(person_name)

        # ALWAYS type Person
        if iteration == 1 and "missing_type" in issues:
            # simulate mistake: do not add rdf:type for some persons
            pass
        else:
            g.add((person_uri, RDF.type, FHKB.Person))

        # label (name)
        g.add((person_uri, RDFS.label, Literal(facts["name"])))

        # birth year
        if facts.get("birth_year") is not None:
            g.add((person_uri, FHKB.hasBirthYear, Literal(int(facts["birth_year"]), datatype=XSD.integer)))

        # father/mother
        if facts.get("father"):
            father_uri = _to_uri(facts["father"])
            g.add((person_uri, FHKB.hasFather, father_uri))
            g.add((person_uri, FHKB.hasParent, father_uri))

        if facts.get("mother"):
            mother_uri = _to_uri(facts["mother"])
            g.add((person_uri, FHKB.hasMother, mother_uri))
            g.add((person_uri, FHKB.hasParent, mother_uri))

        # generic parents
        for p in facts.get("parents", []):
            p_uri = _to_uri(p)
            g.add((person_uri, FHKB.hasParent, p_uri))

    #2) apply fixes based on issues (rule-based “agent behavior”)
    # Example fixes:
    if "missing_type" in issues:
        for person_name in extracted_facts.keys():
          g.add((_to_uri(person_name), RDF.type, FHKB.Person))


    if "wrong_parent_type" in issues:
        for s, _, o in g.triples((None, FHKB.hasFather, None)):
            g.add((o, RDF.type, FHKB.Man))

        for s, _, o in g.triples((None, FHKB.hasMother, None)):
            g.add((o, RDF.type, FHKB.Woman))

    if "too_many_parents" in issues:
        for person_name in extracted_facts:
            person_uri = _to_uri(person_name)

            father = next(g.objects(person_uri, FHKB.hasFather), None)
            mother = next(g.objects(person_uri, FHKB.hasMother), None)

            if father and mother:
                for _, _, parent in list(g.triples((person_uri, FHKB.hasParent, None))):
                    if parent != father and parent != mother:
                        g.remove((person_uri, FHKB.hasParent, parent))

    g.serialize(destination=output_path, format="turtle")
    return output_path