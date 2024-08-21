from typing import List, Dict, Any, Literal, TypedDict
import os
ChatMessage = Dict[Literal["role", "content"], str]
RoleType = Literal["system", "user", "assistant"]

class ChatMessage(TypedDict):
    role: RoleType
    content: str

class ClientNotInstalled(Exception):
    pass

class NotSupportedForModel(Exception):
    pass

class Model:
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name

    def complete_text(self, text: str, stop: List[str] = [], temperature: float = 0.7) -> str:
        raise NotImplementedError
    
    def complete_chat(self, messages: List[ChatMessage]) -> str:
        raise NotImplementedError

class Groq(Model):
    def __init__(self, model_name: str, api_key: str = os.getenv("GROQ_API_KEY")):
        try:
            from groq import Groq
        except ImportError:
            raise ClientNotInstalled("Groq")
        self.groq = Groq(api_key=api_key)
        if model_name not in self.groq.models.list():
            raise Exception(f"Model {model_name} not supported for Groq")
        super().__init__(model_name, api_key)

    def complete_text(self, text: str, stop: List[str] = [], temperature: float = 0.7) -> str:
        raise NotSupportedForModel("Groq does not support text completion")
    
    def complete_chat(self, messages: List[ChatMessage]) -> str:
        response = self.groq.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        return response.choices[0].message.content

class OpenRouter(Model):
    def __init__(self, model_name: str, api_key: str = os.getenv("OPENROUTER_API_KEY")):
        try:
            from openai import OpenAI
        except ImportError:
            raise ClientNotInstalled("OpenAI")
        self.openrouter = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        # if model_name not in self.openrouter.models.list():
        #     raise Exception(f"Model {model_name} not supported for OpenRouter")
        super().__init__(model_name, api_key)

    def complete_text(self, text: str, stop: List[str] = [], temperature: float = 0.7) -> str:
        response = self.openrouter.completions.create(
            model=self.model_name,
            prompt=text,
            stop=stop,
            temperature=temperature,
            max_tokens=1024,
        )
        return response.choices[0].text
    
    def complete_chat(self, messages: List[ChatMessage]) -> str:
        response = self.openrouter.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        try:
            return response.choices[0].message.content
        except:
            print(response) # what the fuck
            raise Exception("OpenRouter fucked up")

class VertexAI(Model):
    def __init__(self, model_name: str, project: str = "vertex-ai-sdk-testing", api_key: str = os.getenv("VERTEX_API_KEY"), endpoint: str = "us-central1-aiplatform.googleapis.com", region: str = "us-central1"):
        try:
            from openai import OpenAI
        except ImportError:
            raise ClientNotInstalled("OpenAI")
        self.openai = OpenAI(api_key=api_key, base_url=f"https://{endpoint}/v1beta1/projects/{project}/locations/{region}/endpoints/openapi")
        super().__init__(model_name, api_key)
    
    def complete_text(self, text: str, stop: List[str] = [], temperature: float = 0.7) -> str:
        raise NotSupportedForModel("VertexAI does not support text completion")
    
    def complete_chat(self, messages: List[ChatMessage]) -> str:
        response = self.openai.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        return response.choices[0].message.content

class OpenAI(Model):
    def __init__(self, model_name: str, api_key: str = os.getenv("OPENAI_API_KEY"), base_url: str = None):
        try:
            from openai import OpenAI
        except ImportError:
            raise ClientNotInstalled("OpenAI")
        self.openai = OpenAI(api_key=api_key, base_url=base_url)
        #if model_name not in self.openai.models.list():
        #    raise Exception(f"Model {model_name} not supported for OpenAI")
        super().__init__(model_name, api_key)

    def complete_text(self, text: str, stop: List[str] = [], temperature: float = 0.7) -> str:
        response = self.openai.completions.create(
            model=self.model_name,
            prompt=text,
            stop=stop,
            temperature=temperature,
            max_tokens=1024,
        )
        return response.choices[0].text
    
    def complete_chat(self, messages: List[ChatMessage]) -> str:
        response = self.openai.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        return response.choices[0].message.content

class Anthropic(Model):
    def __init__(self, model_name: str, api_key: str = os.getenv("ANTHROPIC_API_KEY"), base_url: str = "https://api.anthropic.com"):
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ClientNotInstalled("Anthropic")
        self.anthropic = Anthropic(api_key=api_key, base_url=base_url)
        super().__init__(model_name, api_key)

    def complete_text(self, text: str, stop: List[str] = [], temperature: float = 0.7) -> str:
        raise NotSupportedForModel("Anthropic does not support text completion")
    
    def complete_chat(self, messages: List[ChatMessage]) -> str:
        message = self.anthropic.messages.create(
            max_tokens=1024,
            model=self.model_name,
            messages=messages,
        )
        return message.content