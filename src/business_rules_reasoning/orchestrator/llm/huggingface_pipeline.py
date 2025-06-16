from typing import List, Dict, Any

from .prompt_templates.base_prompt_templates import BasePromptTemplates
from .llm_pipeline_base import LLMPipelineBase
from ...utils.kwargs_utils import merge_kwargs

class HuggingFacePipeline(LLMPipelineBase):
    def __init__(self, model_name: str, tokenizer, model, device=None, prompt_templates: BasePromptTemplates = None, **kwargs):
        from transformers import pipeline

        super().__init__(model_name, prompt_templates)

        self.kwargs = kwargs
        self.model_name = model_name
        self.tokenizer = tokenizer
        self.model = model
        self.device = device
        self.generator = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer, device=self.device, return_full_text=False)

    def prompt_text_generation(self, prompt: str, **kwargs) -> str:
        args = merge_kwargs(self.kwargs, kwargs)
        response = self.generator(prompt, **args)[0]['generated_text']
        return response
