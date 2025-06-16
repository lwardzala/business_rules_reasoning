from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .prompt_templates.base_prompt_templates import BasePromptTemplates
import logging

class LLMPipelineBase(ABC):
    def __init__(self, model_name, prompt_templates: BasePromptTemplates = None):
        self.templates = self._resolve_templates(prompt_templates, model_name)

    @property
    def templates(self) -> BasePromptTemplates:
        return self._templates

    @templates.setter
    def templates(self, value):
        self._templates = value

    @staticmethod
    def _resolve_templates(prompt_templates, model_name):
        if prompt_templates is not None:
            return prompt_templates
        if "llama" in model_name.lower():
            from .prompt_templates import LlamaPromptTemplates
            logging.info(f"[LLMPipelineBase] Automatically detected a Llama model '{model_name}'. LlamaPromptTemplates is used.")
            return LlamaPromptTemplates
        else:
            from .prompt_templates import DefaultPromptTemplates
            logging.info(f"[LLMPipelineBase] Could not find specific prompt templates for model '{model_name}'. DefaultPromptTemplates is used instead.")
            return DefaultPromptTemplates

    @abstractmethod
    def prompt_text_generation(self, prompt: str, **kwargs) -> str:
        pass