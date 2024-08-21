from models import Groq, OpenAI, OpenRouter, VertexAI, Anthropic

# change these!

DATASET_NAME = "anthracite-org/kalo-opus-instruct-22k-no-refusal"
CHAT_HISTORY_COLUMN = "conversations"
OUTPUT_COLUMN = "rejected"
SPLIT = "train"
OUTPUT_DATASET_NAME = "fizztesting/kalo-opus-instruct-22k-no-refusal-ktoed"

# MODEL = OpenRouter("google/gemma-2-9b-it")
# MODEL = VertexAI("meta/llama3-405b-instruct-maas", project="lyrical-beach-431220-r0")
# MODEL = OpenAI("gpt-4-1106-preview")
# MODEL = Anthropic("claude-3-opus-20240229", base_url="https://dataset.scylla.wtf/proxy/anthropic")
MODEL = OpenAI("anthracite-org/magnum-v2-12b", base_url="https://ambien-homeless-italiano-sigma.trycloudflare.com/v1")