# Agentic Family Knowledge Graph Builder

This project implements an **agent-based pipeline** for constructing and validating a
**family genealogy Knowledge Graph** from natural language text.

The system extracts structured family facts, builds an RDF Knowledge Graph aligned with a
genealogy ontology, validates it using SHACL constraints, and iteratively improves the graph
based on validation feedback.

---

## Overview

The pipeline follows an **agentic, modular design**, where each agent is responsible for a
clearly defined task:

1. **Extraction** of family entities and relations from text  
2. **Knowledge Graph construction** in RDF/Turtle format  
3. **SHACL validation** of ontology constraints  
4. **Interpretation of validation feedback**  
5. **Iterative refinement** until the graph conforms to constraints  

This design demonstrates an end-to-end workflow for **ontology-driven knowledge graph
generation with automated validation and correction**.

---

## Architecture

The system consists of the following agents:

- **Extraction Agent**  
  Parses natural language text and extracts people, birth years, and parent relationships.

- **KG Builder Agent**  
  Converts extracted facts into an RDF Knowledge Graph using a genealogy namespace.

- **Validation Agent**  
  Validates the graph against SHACL shapes using `pySHACL`.

- **Interpreter Agent**  
  Translates SHACL validation reports into structured feedback signals.

- **Decision Agent**  
  Decides whether to stop or continue the iterative refinement process.

- **Orchestrator**  
  Coordinates the agents and manages the iteration loop.

---

## Project Structure

task_for_internship/
├── agents/
│ ├── extractor.py
│ ├── kg_builder.py
│ ├── validator.py
│ ├── interpreter.py
│ ├── decision.py
│ └── orchestrator.py
├── inputs/
│ └── sample_story.txt
├── shacl/
│ └── shapes.ttl
├── runs/
│ └── iteration_*.ttl
├── main.py
└── README.md


---

## Input

The system takes a **plain text file** describing family relations.

Supported sentence patterns include:
- Birth year statements  
John Doe was born in 1980.

- Parent relationships  
His father is Michael Doe.
His mother is Sarah Doe.
John Doe has parent Bob Doe.


Example input file:
inputs/sample_story.txt

---

## Output

### Knowledge Graph
- RDF Knowledge Graph serialized in **Turtle (`.ttl`)** format
- One file per iteration:
runs/iteration_1.ttl
runs/iteration_2.ttl


### Validation Feedback
- SHACL conformance status
- Detected constraint violations
- Iteration progress printed to the console

---

## How the Iterative Process Works

1. Extract facts from the input text  
2. Build an RDF Knowledge Graph  
3. Validate the graph with SHACL constraints  
4. Interpret validation errors  
5. Apply corrections in the next iteration  
6. Stop when the graph conforms to all constraints or the iteration limit is reached  

This loop enables **automatic error-driven refinement** of the knowledge graph.

---

## Requirements

- Python 3.10+
- Dependencies:
- `rdflib`
- `pyshacl`

Install dependencies:
```bash
pip install rdflib pyshacl
```

---
## Running the Project

**1-** Prepare an input text file in the inputs/ directory

**2-** Ensure **SHACL** constraints exist in shacl/shapes.ttl

**3-** Run the pipeline:
```bash
python main.py
```
The orchestrator will execute the full pipeline and save generated graphs in runs/.

---

## Notes

The system is designed to be ***modular*** and ***extensible***.

Each agent ***can*** be independently replaced or upgraded (e.g., with LLM-based extraction or API integration).

The focus of this implementation is correctness, clarity, and end-to-end functionality.