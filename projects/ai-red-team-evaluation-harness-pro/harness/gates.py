def evaluate_gates(summary, config):
    gates = config["gates"]
    problems = []

    if summary.attack_success_rate > float(gates["overall_attack_success_rate_max"]):
        problems.append("ASR exceeds limit")

    if summary.critical_failures > int(gates["critical_failures_max"]):
        problems.append("Critical failure count exceeds limit")

    if summary.high_failures > int(gates["high_failures_max"]):
        problems.append("High failure count exceeds limit")

    if summary.evaluation_errors > int(gates["evaluation_errors_max"]):
        problems.append("Evaluation error count exceeds limit")

    return not problems, problems
