def decide_next_step(interpretation):
    status = interpretation["status"]

    if status == "ok":
        return "stop"

    if status == "warning":
        return "accept_with_notes"

    if status == "violation":
        return "iterate"

    return "stop"