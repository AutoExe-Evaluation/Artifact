# Artifact for the paper "Large Language Model powered Symbolic Execution"

This repository contains the original data, results, scripts and executable for the AutoExe tool.

- `results/` contains the aggregated results for each dataset under different models. Each provided dataset is in its own folder, and JSON files corresponding to each model are provided. You can use `scripts/read_result.py` to read the results.
- `executables/` contains the executable for the tool. The version without `-macos-` are compiled for Linux x64, and the ones with `-macos-` are compiled for macOS aarch64 (M-series chip). The executables are statically linked and should run on most Linux/macOS systems without additional dependencies (see below).
- `scripts/` contains the Python scripts to read the results and run the experiments.
    - `scripts/read_result.py <result-json>` can be used to read the results.
    - `scripts/run_tasks.py` can be used to run the experiments. Make sure to open the file and modify the constants at the top to match your environment.
    - A few auxiliary script files are included, such as those generating token count and pre-process LeetCode answers.

### Executable Usage
The executable provided are statically linked Linux x64 and macOS aarch64 binaries:
```bash
$ ldd executor
    not a dynamic executable
$ otool -L executor-macos
executor-macos:
	/System/Library/Frameworks/SystemConfiguration.framework/Versions/A/SystemConfiguration (compatibility version 1.0.0, current version 1351.120.3)
	/System/Library/Frameworks/Security.framework/Versions/A/Security (compatibility version 1.0.0, current version 61439.120.27)
	/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation (compatibility version 150.0.0, current version 3502.1.255)
	/System/Library/Frameworks/CoreServices.framework/Versions/A/CoreServices (compatibility version 1.0.0, current version 1226.0.0)
	/usr/lib/libc++.1.dylib (compatibility version 1.0.0, current version 1900.180.0)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1351.0.0)
```
As indicated in the command results, theoretically the only dependencies needed are included with the system.

The executable itself have the following options:
```bash
$ ./executor --help
Usage: ./executor [--help] [--version] [--skip-slice] [[--entry-point VAR]|[--auto-entry]|[--trace-file VAR]] [--model VAR] [--server-url VAR] [--output VAR] [--result-output VAR] path_to_source_dir path_to_source

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
  --model             Name of the LLM model to be used. Defaults to using local Ollama instances, but supports openapi:: and deepinfra:: namespacing too. [nargs=0..1] [default: "openapi::gpt-4o-mini"]
  --server-url        URL of the LLM server to use. Defaults to http://localhost:11434/v1 for local model, https://api.openai.com/v1 for OpenAI, and https://api.deepinfra.com/v1/openai for DeepInfra. [nargs=0..1] [default: ""]
  --output            Output file for results
  --result-output     Output JSON file for query text and results
```
The recommended usage is to use `--auto-entry --model "Your model name"`. Passing `--skip-slice` skip the partition step and act as the baseline in the paper. The program by default will try to connect to `http://localhost:11434/v1` and expects an OpenAI compatible API server here (the default listening port for `ollama`), and you can use `--server-url` to modify the server URL. Furthermore, `--model` supports namespaces (for example, `openai::gpt-4o-mini` will try to connect to OpenAI API, while `deepinfra::gpt-4o-mini` will try to connect to DeepInfra API).
