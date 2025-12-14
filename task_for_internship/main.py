from agents.orchestrator import run_pipeline

if __name__ == "__main__":
    run_pipeline(
        input_text_path="inputs/sample_story.txt",
        shapes_path="shacl/shapes.ttl",
        max_iterations=3
    )