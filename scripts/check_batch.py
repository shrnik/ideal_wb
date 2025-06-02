from http import client
from openai_client import openai_client

client = openai_client

batch = client.batches.retrieve("batch_682f679868148190afb77da97f6a0402")
print(batch)
