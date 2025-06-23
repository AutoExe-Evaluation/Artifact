import json
import sys
from math import sqrt
import tiktoken


ENCODING = tiktoken.encoding_for_model("gpt-4o-mini")


def average(data):
    assert len(data) > 0, data
    return sum(data) / len(data)


def stddev(data):
    """ Calculate standard deviation """
    data_list = list(data)
    assert len(data_list) > 0, data_list
    n = len(data_list)
    avg = average(data_list)
    if n == 1:
        return 0.0
    return sqrt(sum((elem - avg) * (elem - avg) / (n - 1) for elem in data_list))


def process(text):
    while "# FILE: " in text:
        index = text.find("# FILE: ")
        index2 = text.find("\n", index)
        text = text[:index].rstrip() + text[index2 + 1:].lstrip()
    while "unreachable()" in text:
        index = text.find("unreachable()")
        index2 = text.find("\n", index)
        text = text[:index].rstrip() + text[index2 + 1:].lstrip()
    return text


def get_avg_token(texts):
    lens = [len(ENCODING.encode(process(text))) for text in texts]
    return average(lens), stddev(lens)


if len(sys.argv) != 2:
    print("Usage: read_token.py <token_file>")
    sys.exit(1)
json_dict = json.load(open(sys.argv[1], "r"))

all_cases = []
first_unsat = []
for test_case in json_dict:
    for elem in test_case:
        all_cases.append(elem["query_text"])

    if any(elem["query_result"] == "unsat" for elem in test_case):
        first_unsat.append(min(
            [elem for elem in test_case if elem["query_result"] == "unsat"],
            key=lambda elem: len(elem["query_text"])
        )["query_text"])
    else:
        first_unsat.append(max(
            test_case, key=lambda elem: len(elem["query_text"])
        )["query_text"])

print("Token Count:", get_avg_token(first_unsat))
