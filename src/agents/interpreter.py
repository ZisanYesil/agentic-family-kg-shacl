def interpret_results(conforms, report_text):
    """
    Interprets SHACL validation output into symbolic issues.
    """

    if conforms:
        return {
            "status": "ok",
            "issues": [],
            "message": "Data conforms to all SHACL constraints."
        }

    issues = set()

    #Pattern-based interpretation (rule-based, explainable)
    if "rdfs:label" in report_text:
        issues.add("missing_label")

    if "hasFather" in report_text or "hasMother" in report_text:
        issues.add("wrong_parent_type")

    if "MinCountConstraintComponent" in report_text:
        issues.add("cardinality_violation")

    if "class" in report_text or "rdf:type" in report_text:
        issues.add("missing_type")

    if "MaxCountConstraintComponent" in report_text:
        issues.add("too_many_parents")

    if not issues:
        issues.add("unknown_violation")

    return {
        "status": "violation",
        "issues": list(issues),
        "message": f"Detected issues: {', '.join(issues)}"
    }
