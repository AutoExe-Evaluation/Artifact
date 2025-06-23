# Artifact for the paper "Large Language Model powered Symbolic Execution"

This repository contains the original data, results, scripts and executable for the AutoExe tool.

- `raw-output` contains the raw response from LLMs for one of the runs of the tool.
- `results` contains the aggregated results for each dataset under different models.
- `scripts` contains the executable for the tool and Python scripts to read the results.
    - `executor` is the executable for the AutoExe tool. Without suffix it can handle C inputs, and `executor-py`/`executor-java` can handle Python/Java inputs.
    - `read_result.py <result-json>` can be used to read the results.
    - A few auxiliary script files are included, such as those generating token count and pre-process LeetCode answers.

### Executable Usage
The executable provided are statically linked Linux x64 binaries:
```bash
$ ldd executor
	linux-vdso.so.1 (0x00007ffc8d1e3000)
	libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x0000701247400000)
	libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x000070124aa43000)
	libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x000070124aa23000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x0000701247000000)
	/lib64/ld-linux-x86-64.so.2 (0x000070124ab4f000)
$ ./executor --help
Usage: ./executor [--help] [--version] [--skip-slice] [[--entry-point VAR]|[--auto-entry]|[--trace-file VAR]] [--model VAR] [--output VAR] [--result-output VAR] path_to_source_dir path_to_source

Positional arguments:
  path_to_source_dir  Directory containing the sources
  path_to_source      File containing the source to analyze

Optional arguments:
  -h, --help          shows help message and exits
  -v, --version       prints version information and exits
  --skip-slice        Skip slicing and send the whole program to LLM
  --entry-point       Name of the function that serves as the entry point [nargs=0..1] [default: "entry"]
  --auto-entry        Automatically select the last function as the entry point
  --trace-file        Use an existing trace file
  --model             Name of the LLM model to be used [nargs=0..1] [default: "gpt-4o-mini"]
  --output            Output file for results
  --result-output     Output JSON file for query text and results
```
The recommended usage is to use `--auto-entry --model "Your model name"`. Passing `--skip-slice` skip the partition step and act as the baseline in the paper. The program by default will try to connect to `http://localhost:11434/v1` and expects an OpenAI compatible API server here (the default listening port for `ollama`).
