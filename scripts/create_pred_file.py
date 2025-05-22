import os
import json
import pandas as pd


def get_system_prompt() -> str:
    return (
        "You are an expert at analysing research paper for impact in development economics.\nFoe a given title, abstract and authors, you need to find research design, research method and intervention used in the study\n\nResearch Design could be one the following:\nQuasi-experimental\nExperimental\nQualitative\n\nResearch method could be one the following:\nFixed effects (incl. DiD)\nStatistical matching\nInstrumental variable estimation\nRegression discontinuity design\nRandomised controlled trial\nSynthetic control\nInterrupted time series analysis\nOutcome harvesting\nOther\n\nOutput should be a valid json with keys: method, design, intervention\n"
    )


def get_user_prompt(abstract: str, title: str) -> str:
    return f"Title: {title}\nAbstract: {abstract}"


csv = "data/initial_data.csv"


def get_csv_data(csv: str):
    df = pd.read_csv(csv)
    return df


def replace_nbsp(text):
    return text.replace('\u00a0', ' ').replace('\u2011', '-').replace('\u2014', '--')


def get_input_data(df: pd.DataFrame):
    input_data = []
    for index, row in df.iterrows():
        title = row["Title"]
        abstract = row["Abstract"]
        api_input = {
            "custom_id": f"row-{index}",
            "url": "/v1/chat/completions",
            "method": "POST",
            "body": {
                "model": "gpt-4.1",
                "messages": [
                    {"role": "system", "content": [{
                        "type": "text",
                        "text": get_system_prompt()
                    }]},
                    {"role": "user", "content": [{
                        "type": "text",
                        "text": replace_nbsp(get_user_prompt(
                            abstract, title))}
                    ]},
                ],
                "response_format": {
                    "type": "text"
                },
                "temperature": 1,
                "max_completion_tokens": 200,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0
            },
        }
        input_data.append(api_input)
    return input_data


def get_batch_file():
    df = get_csv_data(csv)
    input_data = get_input_data(df[:2000])
    batch_file = "data/batch_input.jsonl"
    os.makedirs(os.path.dirname(batch_file), exist_ok=True)

    with open(batch_file, "w") as f:
        for item in input_data:
            f.write(json.dumps(item) + "\n")


get_batch_file()
