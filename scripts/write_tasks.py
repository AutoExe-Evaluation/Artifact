import os
import json
import shutil

if os.path.exists("../../python-tests/"):
    shutil.rmtree("../../python-tests/")
os.mkdir("../../python-tests/")

with open("DREval_data.jsonl", "r") as fp:
    for line in fp:
        json_dict = json.loads(line)
        task_id = int(json_dict["task_id"][json_dict["task_id"].rfind("/") + 1:].strip())
        code = json_dict["code"]
        if task_id >= 85:
            continue

        # Remove imports
        code = code[code.index("def"):]
        while "from" in code:
            import_index = code.index("from")
            import_end = code.index("\n", import_index)
            code = code[:import_index] + code[import_end + 1:]
        while "import" in code:
            import_index = code.index("import")
            import_end = code.index("\n", import_index)
            code = code[:import_index] + code[import_end + 1:]

        # Remove """s
        code = code.replace("'''", '"""')
        comment = []
        while '"""' in code:
            triple_index = code.index('"""')
            triple_index2 = code.index('"""', triple_index + 3)
            comment.append(code[triple_index + 3:triple_index2].strip())
            code = code[:triple_index] + code[triple_index2 + 3:].lstrip()
        comment_str = " ".join(comment).replace("\n", " ")
        while "  " in comment_str:
            comment_str = comment_str.replace("  ", " ")

        # Find out all the arguments
        if "\ndef" in code:
            last_def = code.rindex("\ndef")
        else:
            last_def = 0
        last_argstart = code.index("(", last_def)
        last_argend = code.index(")", last_argstart)
        splits = code[last_argstart + 1:last_argend].split(",")
        vars = []
        for split in splits:
            split = split.strip()
            if ":" in split:
                split = split[:split.index(":")].strip()
            vars.append(split)

        with open(f"../../python-tests/task{task_id:>02}_desc.py", "w") as fp2:
            fp2.write(code + f"\n    assert func(_result)  # POST: func is equivalent to: {comment_str}")
