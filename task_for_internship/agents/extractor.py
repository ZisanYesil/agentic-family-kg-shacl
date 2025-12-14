import re
from dataclasses import dataclass, asdict
from typing import Dict, List, Any


@dataclass
class PersonFacts:
    """Intermediate representation extracted from text."""
    name: str
    birth_year: int | None = None
    father: str | None = None
    mother: str | None = None
    parents: List[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["parents"] = d["parents"] or []
        return d


def _norm_name(s: str) -> str:
    # Keep it simple, consistent normalization
    return " ".join(s.strip().split())


def extract_facts(text: str) -> Dict[str, Dict[str, Any]]:
    """
    Rule-based extraction from simple English sentences.

    Output format:
    {
      "John Doe": {"name": "John Doe", "birth_year": 1980, "father": "...", "mother": "...", "parents": [...]},
      ...
    }
    """
    people: Dict[str, PersonFacts] = {}

    def get_person(name: str) -> PersonFacts:
        name = _norm_name(name)
        if name not in people:
            people[name] = PersonFacts(name=name, parents=[])
        if people[name].parents is None:
            people[name].parents = []
        return people[name]

    # Patterns
    born_pat = re.compile(r"^(?P<child>.+?) was born in (?P<year>\d{4})\.$")
    father_pat = re.compile(r"^His father is (?P<father>.+?)\.$")
    mother_pat = re.compile(r"^His mother is (?P<mother>.+?)\.$")
    parent_pat = re.compile(r"^(?P<child>.+?) has parent (?P<parent>.+?)\.$")

    last_subject: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        m = born_pat.match(line)
        if m:
            child = _norm_name(m.group("child"))
            year = int(m.group("year"))
            get_person(child).birth_year = year
            last_subject = child
            continue

        m = father_pat.match(line)
        if m and last_subject:
            father = _norm_name(m.group("father"))
            get_person(last_subject).father = father
            #create node for father
            get_person(father)
            last_subject = last_subject
            continue

        m = mother_pat.match(line)
        if m and last_subject:
            mother = _norm_name(m.group("mother"))
            get_person(last_subject).mother = mother
            get_person(mother)
            last_subject = last_subject
            continue

        m = parent_pat.match(line)
        if m:
            child = _norm_name(m.group("child"))
            parent = _norm_name(m.group("parent"))
            pf = get_person(child)
            pf.parents.append(parent)
            get_person(parent)
            last_subject = child
            continue

        # If a line doesn't match, we ignore
        # print(f"[extractor] Unparsed line: {line}")

    # Return dict-of-dicts to make it easy for other agents
    return {name: facts.to_dict() for name, facts in people.items()}


def extract_facts_from_file(path: str) -> Dict[str, Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return extract_facts(f.read())