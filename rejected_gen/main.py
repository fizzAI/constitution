# pure and utter garbage
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import copy, random
from models import Model
from typing import List, Dict, Literal, TypedDict

ChatMessage = Dict[Literal["from", "value"], str]
RoleType = Literal["system", "human", "gpt"]

class RejectedGenerator():
    def __init__(self, model: Model):
        self.model = model

    def generate_rejected(self, chat_history: List[ChatMessage]) -> List[ChatMessage]:
        for msg in chat_history:
            if msg['from'] == "human":
                msg['from'] = 'user'
            if msg['from'] == 'gpt':
                msg['from'] = 'assistant'

        # FIXME: unhardcode this
        EOT_TOKEN = "<|im_end|>"
        CONTEXT = f"""<|im_start|>{chat_history[0]['from']}
{chat_history[0]['value']}<|im_end|>
<|im_start|>{chat_history[1]['from']}
{chat_history[1]['value']}<|im_end|>
"""
        
        if chat_history[1]['from'] == 'user':
            CONTEXT += "<|im_start|>assistant\n"
        else:
            CONTEXT += "<|im_start|>user\n"


        new_chat_history = chat_history[:2]
        generation_count = len(chat_history[2:])

        for _ in range(generation_count):
            print(new_chat_history)
            res = self.model.complete_text(CONTEXT, stop=[EOT_TOKEN], temperature=random.choice(range(0.9,1.0,0.5)))
            this_role = ""
            if new_chat_history[-1]['from'] == 'user':
                this_role = "assistant"
            else:
                this_role = "user"
            new_chat_history += [{
                "from": this_role,
                "value": res
            }]
            CONTEXT += res + f"<|im_end|>\n<|im_start|>{new_chat_history[-2]['from']}\n"
        
        return new_chat_history

if __name__ == "__main__":
    import config

    from datasets import load_dataset
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from tqdm import tqdm

    dataset = load_dataset(config.DATASET_NAME, split=config.SPLIT).shuffle().select(range(10))

    rejected_gen = RejectedGenerator(config.MODEL)

    res = rejected_gen.generate_rejected(copy.deepcopy(dataset[0][config.CHAT_HISTORY_COLUMN]))

    print("ORIGINAL:")
    print(dataset[0][config.CHAT_HISTORY_COLUMN])
    print("MAGPIED:")
    print(res)