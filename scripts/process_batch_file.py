from http import client
from openai_client import openai_client

client = openai_client

batch_input_file = client.files.create(
    file=open("data/batch_input.jsonl", "rb"),
    purpose="batch"
)

print(batch_input_file)


b = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
        "description": "nightly eval job"
    }
)

print(b)

# batch = client.batches.retrieve("batch_682e95dcd49c819098cfebb0f0c2aad2")
# print(batch)
