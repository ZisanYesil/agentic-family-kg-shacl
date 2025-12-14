from agents.extractor import extract_facts_from_file
from agents.kg_builder import build_kg
from agents.validator import run_validation
from agents.interpreter import interpret_results
from agents.decision import decide_next_step


def run_pipeline(input_text_path, shapes_path, max_iterations=3):
    extracted = extract_facts_from_file(input_text_path)

    issues = []  # start empty; iteration 1 is naive
    for iteration in range(1, max_iterations + 1):
        print(f"\n--- Iteration {iteration} ---")

        kg_path = build_kg(iteration, issues, extracted)
        conforms, report_text = run_validation(kg_path, shapes_path)

        interpretation = interpret_results(conforms, report_text)
        decision = decide_next_step(interpretation)

        print("Interpretation:", interpretation["message"])
        print("Decision:", decision)

        # update issues for next iteration
        issues = interpretation.get("issues", [])

        if decision in ("stop", "accept_with_notes"):
            break