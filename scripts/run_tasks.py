import glob
import json
import os
import subprocess
import time


SRC_DIR = "path/to/dataset/RQ1/REval-Desc/"
RESULTS = "output.json"
MODEL = "llama3.1:8b"
EXECUTABLE = "../executables/executor"


json_set = set()
test_result = []
if os.path.exists(RESULTS):
    json_dict = json.load(open(RESULTS, "r"))
    json_set = set(x["file_name"] for x in json_dict)
    test_result = json_dict
#     os.remove(RESULTS)


subjects = list(glob.glob(os.path.join(SRC_DIR, "*.c")))
subjects += list(glob.glob(os.path.join(SRC_DIR, "*.py")))
subjects += list(glob.glob(os.path.join(SRC_DIR, "*.java")))
for test_case in sorted(subjects):
    file_name = os.path.basename(test_case)
    suffix = file_name.split(".")[-1]
    if suffix == "c":
        suffix = ""
    else:
        suffix = "-" + suffix
    if file_name in json_set:
        print(f"=====> Skipping {file_name}...")
        continue

    print(f"\n\n=====> Testing {file_name}...")
    cmd = [EXECUTABLE + suffix, SRC_DIR, test_case, "--auto-entry", "--output", "result.txt", "--model", MODEL]
    while not os.path.exists("result.txt"):
        start_time = time.time()
        popen = subprocess.run(cmd, text=True)
        elapsed = time.time() - start_time
        # if popen.returncode != 0:
        #     raise subprocess.CalledProcessError(popen.returncode, cmd)

    with open("result.txt", "r") as fp:
        result = fp.read().strip()
        splits = result.split("\n")
        assert len(splits) == 2, result
        result, lens = splits
    os.remove("result.txt")

    print(f"\n\n=====> SKIP-SLICE Testing {file_name}...")
    while not os.path.exists("result.txt"):
        start_time = time.time()
        popen = subprocess.run(cmd + ["--skip-slice"], text=True)
        elapsed_baseline = time.time() - start_time
        # if popen.returncode != 0:
        #     raise subprocess.CalledProcessError(popen.returncode, cmd)

    with open("result.txt", "r") as fp:
        result_baseline = fp.read().strip()
        splits = result_baseline.split("\n")
        assert len(splits) == 2, result
        result_baseline, lens_baseline = splits
    os.remove("result.txt")

    test_result.append({
        "file_name": file_name,
        "result_autoexe": result.strip(),
        "lens_autoexe": [int(x) for x in lens.strip().split(", ")],
        "time_autoexe": elapsed,
        "result_baseline": result_baseline.strip(),
        "lens_baseline": [int(x) for x in lens_baseline.strip().split(", ")],
        "time_baseline": elapsed_baseline
    })

    with open(RESULTS, "w") as fp:
        json.dump(test_result, fp, indent=4)
