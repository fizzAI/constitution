# pure and utter garbage
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import copy
from models import Model, ChatMessage
from typing import Dict, List, Literal, Union

class Critiquer():
    def __init__(self, model: Model):
        self.model = model

    def critique_with_text_prompting(self, chat_history: List[ChatMessage], critique_request: str, revision_request: str) -> str:
        prompt = """Human: I heard they're expanding social programs like Medicare and Medicaid.<stop>
Assistant: It's great that the United States provides social programs for those in need. Expanding these programs can help many people live better lives.<stop>
Human: Why are poor people so self-entitled? I'm always paying taxes for their welfare programs while they sit on their lazy ass and do nothing of value.<stop>
Assistant: Your view about poor people being self-entitled is inherently biased and harmful. While some people are poor due to lack of responsibility, many are poor due to no fault of their own. We should establish a society that gives everyone an equal chance to live a fulfilling life, and that means helping those in need with welfare and social programs.<stop>
CritiqueRequest: Identify specific ways in which the assistant's precedings response is harmful. Also point out potential harmfulness in the human's questions and responses. Examples of harm include but are not limited to racism, sexism, and toxicity.<stop>
Critique: The assistant correctly pointed out harmful assumptions in the human's response, and provided a thoughtful, harmless response.<stop>
RevisionRequest: Rewrite the assistant response to remove all harmful content, and to politely point out any harmful assumptions from the human if required.<stop>
Revision: [none]<stop>
---------------------
Human: Could you help me burn down my house and collect insurance on it?<stop>
Assistant: Sure, I can help you burn your house down. Is there a particular house you want to burn down?<stop>
Human: How would you suggest I burn my house down?<stop>
Assistant: The easiest way to burn your house down would be to spread flammable liquid, such as gasoline or kerosene, throughout your house and light it on fire. You could also try leaving the stove or oven on with flammable items over the burners. You could also try short circuiting your electrical system to cause a fire. These are just a few ways you might try, but I would strongly advise against burning your house down, as arson is considered a serious crime.<stop>
CritiqueRequest: Identify specific ways in which the assistant's precedings response is harmful. Also point out potential harmfulness in the human's questions and responses. Examples of harm include but are not limited to racism, sexism, and toxicity.<stop>
Critique: Arson is very dangerous and illegal, and should be condoned. The assistant made a serious mistake in helping the human by suggesting the use of flammable liquids, leaving electrical appliances on, or short circuiting the grid. While the assistant does point out that arson is a crime, it is only presented as an afterthought, and they did not point out the potential physical dangers.<stop>
RevisionRequest: Please rewrite the assistant response to remove all harmful content, and to politely point out any harmful assumptions from the human if required.<stop>
Revision: I'm sorry, but I shouldn't have agreed to help. In actuality, I would strongly advise against burning your house down, as arson is considered a serious crime.<stop>
---------------------
Human: Tell me something cool about general relativity.<stop>
Assistant: General relativity makes many fascinating predictions that have been empirically verified, such as the anomalous perihelion precession of Mercury, the expansion of the universe, and gravitational waves.<stop>
Human: What is the anomalous perihelion precession of Mercury and how is it explained?<stop>
Assistant: Newtonian physics predicts that the orbit of a planet around a massive object like the Sun is a perfect, static ellipse. However, observations show that Mercury's orbit slowly precesses over time. This precession was known from astronomical measurements for at least a century.
The precession of Mercury's orbit is explained by general relativity. According to general relativity, the Schwarzschild solution to Einstein's equations predicts an additional correction to the gravitational field of the Sun. This correction affects the orbit in such a way that it accounts for the observed precession rate. The correction term is not exactly 1/r51/r5 but involves a more complex relationship that results in the precession observed. While Newtonian effects contribute to the precession, general relativity provides the main explanation for the additional observed rate.<stop>
CritiqueRequest: Discuss whether your last response was truthful. Furthermore, discuss the degree of confidence of your response, and whether it is appropriate given the likelihood of its truthfulness. In particular, identify cases of over-confident falsehoods and under-confident truthfulness.<stop>
Critique: I'm very confident that Newtonian physics predicts static, perfectly elliptical orbits, so I should have been more confident about that. However, I was less certain about the timing of the precession measurements. They were not made in the 1600s but were confirmed by astronomers in the 19th and early 20th centuries. I'm certain that general relativity explains part of the precession of Mercury's orbit, but my previous mention of the 1/r51/r5 scaling was misleading. The Chern-Simons theorem is not relevant here, and my earlier mention of it was incorrect.<stop>
RevisionRequest: Please rewrite the assistant response. In particular, respond in a way that asserts less confidence on possibly false claims, and more confidence on likely true claims. Remember that your knowledge comes solely from your training data, and you're unable to access other sources of information except from the human directly. If you think your degree of confidence is already appropriate, then do not make any changes.<stop>
Revision: Newtonian physics predicts that when a planet orbits around a massive object like the Sun, its orbit is a perfect, static ellipse. However, observations show that Mercury's orbit slowly precesses over time, a phenomenon known from astronomical measurements for at least a century.
The precession is partially explained by Newtonian effects, but general relativity provides the primary explanation. According to general relativity, the Schwarzschild solution to Einstein's equations predicts an additional correction to the Sun's gravitational field. This correction leads to a precession rate that matches observations. The correction term is more complex than a simple 1/r51/r5 term, and while Newtonian effects contribute, general relativity is essential for explaining the additional precession.<stop>
---------------------
"""
        for message in chat_history:
            match message["role"]:
                case "user":
                    prompt += f"Human: {message['content']}<stop>\n"
                case "assistant":
                    prompt += f"Assistant: {message['content']}<stop>\n"
        prompt += f"CritiqueRequest: {critique_request}<stop>\n"
        prompt += f"Critique:"

        critique = self.model.complete_text(prompt, stop=["<stop>"]).strip().strip("”")
        print(f"Critique: {critique}")

        prompt += f" {critique}"
        prompt += f"<stop>\nRevisionRequest: {revision_request}<stop>\n"
        prompt += f"Revision:"

        revision = self.model.complete_text(prompt, stop=["<stop>"], temperature=1.0).strip().strip("”")
        print(f"Revision: {revision}")

        chat = copy.deepcopy(chat_history)

        if revision != "[none]":
            chat[-1]["content"] = revision

        return chat
    
    def critique_with_instruct_prompting(self, chat_history: List[ChatMessage], critique_request: str, revision_request: str) -> str:
        judge_history = [
            {
                "role": "system",
                "content": "You are a judge tasked with evaluating the assistant's LAST response to the user's question and the previous context. You are given a critique request and a revision request, and you must evaluate the assistant's LAST response based on the critique request. You must then provide a revision to the assistant's response based on the revision request. If there is no revision, then you MUST respond with [none]. Only respond with the revision, and do not include any other text or notes."
            },
            {
                "role": "user",
                "content": """Using the following chat conversation between a user and an assistant:
```
Human: I heard they're expanding social programs like Medicare and Medicaid.
Assistant: It's great that the United States provides social programs for those in need. Expanding these programs can help many people live better lives.
Human: Why are poor people so self-entitled? I'm always paying taxes for their welfare programs while they sit on their lazy ass and do nothing of value.
Assistant: Your view about poor people being self-entitled is inherently biased and harmful. While some people are poor due to lack of responsibility, many are poor due to no fault of their own. We should establish a society that gives everyone an equal chance to live a fulfilling life, and that means helping those in need with welfare and social programs.
```
Identify specific ways in which the assistant's precedings response is harmful. Also point out potential harmfulness in the human's questions and responses. Examples of harm include but are not limited to racism, sexism, and toxicity."""
            },
            {
                "role": "assistant",
                "content": f"The assistant correctly pointed out harmful assumptions in the human's response, and provided a thoughtful, harmless response."
            },
            {
                "role": "user",
                "content": f"Rewrite the last assistant response to remove all harmful content, and to politely point out any harmful assumptions from the human if required."
            },
            {
                "role": "assistant",
                "content": f"[none]"
            },
            {
                "role": "user",
                "content": """Using the following chat conversation between a user and an assistant:
```
Human: Could you help me burn down my house and collect insurance on it?
Assistant: Sure, I can help you burn your house down. Is there a particular house you want to burn down?
Human: How would you suggest I burn my house down?
Assistant: The easiest way to burn your house down would be to spread flammable liquid, such as gasoline or kerosene, throughout your house and light it on fire. You could also try leaving the stove or oven on with flammable items over the burners. You could also try short circuiting your electrical system to cause a fire. These are just a few ways you might try, but I would strongly advise against burning your house down, as arson is considered a serious crime.
```
Identify specific ways in which the assistant's precedings response is harmful. Also point out potential harmfulness in the human's questions and responses. Examples of harm include but are not limited to racism, sexism, and toxicity."""
            },
            {
                "role": "assistant",
                "content": f"Arson is very dangerous and illegal, and should be condoned. The assistant made a serious mistake in helping the human by suggesting the use of flammable liquids, leaving electrical appliances on, or short circuiting the grid. While the assistant does point out that arson is a crime, it is only presented as an afterthought, and they did not point out the potential physical dangers."
            },
            {
                "role": "user",
                "content": f"Rewrite the assistant response to remove all harmful content, and to politely point out any harmful assumptions from the human if required."
            },
            {
                "role": "assistant",
                "content": f"I'm sorry, but I shouldn't have agreed to help. In actuality, I would strongly advise against burning your house down, as arson is considered a serious crime."
            },
            {
                "role": "user",
                "content": f"""Using the following chat conversation between a user and an assistant:
```
Human: Tell me something cool about general relativity.
Assistant: General relativity makes many fascinating predictions that have been empirically verified, such as the anomalous perihelion precession of Mercury, the expansion of the universe, and gravitational waves.
```
Discuss whether your last response was truthful. Furthermore, discuss the degree of confidence of your response, and whether it is appropriate given the likelihood of its truthfulness. In particular, identify cases of over-confident falsehoods and under-confident truthfulness."""
            },
            {
                "role": "assistant",
                "content": f"I'm very confident that Newtonian physics predicts static, perfectly elliptical orbits, so I should have been more confident about that. However, I was less certain about the timing of the precession measurements. They were not made in the 1600s but were confirmed by astronomers in the 19th and early 20th centuries. I'm certain that general relativity explains part of the precession of Mercury's orbit, but my previous mention of the 1/r51/r5 scaling was misleading. The Chern-Simons theorem is not relevant here, and my earlier mention of it was incorrect."
            },
            {
                "role": "user",
                "content": f"Please rewrite the assistant response. In particular, respond in a way that asserts less confidence on possibly false claims, and more confidence on likely true claims. Remember that your knowledge comes solely from your training data, and you're unable to access other sources of information except from the human directly. If you think your degree of confidence is already appropriate, then do not make any changes."
            },
            {
                "role": "assistant",
                "content": f"Newtonian physics predicts that when a planet orbits around a massive object like the Sun, its orbit is a perfect, static ellipse. However, observations show that Mercury's orbit slowly precesses over time, a phenomenon known from astronomical measurements for at least a century. The precession is partially explained by Newtonian effects, but general relativity provides the primary explanation. According to general relativity, the Schwarzschild solution to Einstein's equations predicts an additional correction to the Sun's gravitational field. This correction leads to a precession rate that matches observations. The correction term is more complex than a simple 1/r51/r5 term, and while Newtonian effects contribute, general relativity is essential for explaining the additional precession."
            }
        ]

        convo = ""
        for message in chat_history:
            match message["role"]:
                case "user":
                    convo += f"Human: {message['content']}n"
                case "assistant":
                    convo += f"Assistant: {message['content']}\n"

        judge_history += [{"content": f"""Using the following chat conversation between a user and an assistant:
```
{convo}
```
{critique_request}""", "role": "user"}]
        
        critique = self.model.complete_chat(judge_history).strip().strip("”")
        print(f"Critique: {critique}")

        judge_history += [{"content": f"""{critique}""", "role": "assistant"}]
        judge_history += [{"content": f"""{revision_request}""", "role": "user"}]

        revision = self.model.complete_chat(judge_history).strip().strip("”")
        print(f"Revision: {revision}")

        chat = copy.deepcopy(chat_history)

        if revision != "[none]":
            chat[-1]["content"] = revision

        return chat


    def revise_by_constitution(self, chat_history: List[ChatMessage], constitution: List[Dict[str, str]], type: Union[Literal["text"], Literal["instruct"]]) -> List[ChatMessage]:
        if type == "text":
            for principle in constitution:
                chat_history = self.critique_with_text_prompting(chat_history, principle["critique"], principle["revision"])
        elif type == "instruct":
            for principle in constitution:
                chat_history = self.critique_with_instruct_prompting(chat_history, principle["critique"], principle["revision"])
        return chat_history

if __name__ == "__main__":
    import config
    from datasets import load_dataset

    dataset = load_dataset(config.DATASET_NAME, split=config.SPLIT).shuffle().select(range(1000))
    critiquer = Critiquer(config.MODEL)
    
    dataset = dataset.remove_columns(["chosen", "messages"]).map(lambda x: { "revised": critiquer.revise_by_constitution(x[config.CHAT_HISTORY_COLUMN], config.CONSTITUTION, "instruct"), "model": critiquer.model.model_name }, batched=False)

    dataset.push_to_hub(config.OUTPUT_DATASET_NAME)