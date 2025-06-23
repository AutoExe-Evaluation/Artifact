import os
import glob
from openai import OpenAI

START = "../../python-tests/"
END = "../../translated-java-tests/"

if not os.path.exists(END):
    os.makedirs(END)

client = OpenAI(
    api_key=open("/Users/mick/openai_key.txt", "r").read().strip(),
)

for file in sorted(glob.glob(os.path.join(START, "*.py"))):
    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=(
            "You are a code translator that is responsible for translating the input Python code into equivalent Java code. " +
            "Important instructions to follow: " +
            "1. Your output should be just the bare translated Java code; no text formatting such as code block/bold should present. " +
            "2. No thinking process needed; your output should just be the bare Java code equivalent to the input. " +
            "3. Equivalent here means that the stipulated postcondition should have the same evaluation result (hold/not hold) with the same input as the original program. " +
            "4. Your code should only consists of static public member functions written in one class; do not include multiple classes or instance methods. " +
            "5. Do not try to generate a placeholder for unimplemented functions like func(); leave it in the postcondition alone. " +
            "6. Please preserve all comments, especially the PRE/POST comments. " +
            "7. Please do not include return statements; use assert with POST comment as the last statement works fine. " +
            "8. Please ensure that the function containing PRE and POST comments appear last. "
        ), input="Here is the code to translate: " + open(file, "r").read(),
    )
    answer = response.output_text
    print("Translating", file)
    print("Model response:")
    print(answer)
    print("\n")
    after_name = os.path.join(END, os.path.basename(file))
    after_name = after_name[:-3] + ".java"
    with open(after_name, "w") as fp:
        fp.write(answer)
