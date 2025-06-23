import json
import sys


EXPECTED_UNSAT = {
    "question0007.c",
    "question0019.c",
    "question0026.c",
    "question0027.c",
    "task36.py",
    "task42.c",
    "task42.py"
}


def print_max(result_dict):
    result_list = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    print(", ".join(f"{k}: {v}" for k, v in result_list))


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <result-json>")
    sys.exit(1)

json_dict = json.load(open(sys.argv[1], "r"))
autoexe_cnt = {}
baseline_cnt = {}
for elem in json_dict:
    if "result_autoexe" in elem:
        max_key = elem["result_autoexe"]
        if elem["file_name"] in EXPECTED_UNSAT:
            max_key = "unsat" if max_key == "sat" else "sat"
        if max_key not in autoexe_cnt:
            autoexe_cnt[max_key] = 0
        autoexe_cnt[max_key] += 1

    max_key = elem["result_baseline"] if "result_baseline" in elem else elem["result"]
    if elem["file_name"] in EXPECTED_UNSAT:
        max_key = "unsat" if max_key == "sat" else "sat"
    if max_key not in baseline_cnt:
        baseline_cnt[max_key] = 0
    baseline_cnt[max_key] += 1

print("AutoExe: ", end="")
print_max(autoexe_cnt)
print("Baseline: ", end="")
print_max(baseline_cnt)
