from transformers import pipeline
from typing import List, Dict, Any
from .llm_pipeline_base import LLMPipelineBase
from ...utils.kwargs_utils import merge_kwargs

class HuggingFacePipeline(LLMPipelineBase):
    def __init__(self, model_name: str, tokenizer, model, device, **kwargs):
        self.model_name = model_name
        self.tokenizer = tokenizer
        self.model = model
        self.kwargs = kwargs
        self.device = device
        self.generator = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer, device=self.device, return_full_text=False)

    def prompt_text_generation(self, prompt: str, **kwargs) -> str:
        args = merge_kwargs(self.kwargs, kwargs)
        response = self.generator(prompt, **args)[0]['generated_text']
        return response

    def prompt_summarization(self, prompt: str, **kwargs) -> str:
        args = merge_kwargs(self.kwargs, kwargs)
        summarizer = pipeline("summarization", model=self.model, tokenizer=self.tokenizer, device=self.device, return_full_text=False)
        response = summarizer(prompt, **args)[0]['summary_text']
        return response

    def prompt_question_answering(self, question: str, context: str, **kwargs) -> str:
        args = merge_kwargs(self.kwargs, kwargs)
        qa_pipeline = pipeline('question-answering', model=self.model, tokenizer=self.tokenizer, device=self.device, return_full_text=False)
        response = qa_pipeline(question=question, context=context, **args)[0]['answer']
        return response

    def prompt_text2text_generation(self, prompt: str, **kwargs) -> str:
        args = merge_kwargs(self.kwargs, kwargs)
        text2text_generator = pipeline('text2text-generation', model=self.model, tokenizer=self.tokenizer, device=self.device, return_full_text=False)
        response = text2text_generator(prompt, **args)[0]['generated_text']
        return response

    def prompt_table_question_answering(self, query: str, table: Dict[str, List[Any]], **kwargs) -> str:
        args = merge_kwargs(self.kwargs, kwargs)
        table_qa_pipeline = pipeline('table-question-answering', model=self.model, tokenizer=self.tokenizer, device=self.device, return_full_text=False)
        response = table_qa_pipeline(query=query, table=table, **args)[0]['answer']
        return response

    def prompt_text_classification(self, text: str, **kwargs) -> str:
        args = merge_kwargs(self.kwargs, kwargs)
        text_classifier = pipeline('text-classification', model=self.model, tokenizer=self.tokenizer, device=self.device, return_full_text=False)
        response = text_classifier(text, **args)[0]['label']
        return response
