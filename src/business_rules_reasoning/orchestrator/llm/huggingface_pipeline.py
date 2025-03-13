from transformers import pipeline, TextGenerationPipeline, QuestionAnsweringPipeline, Text2TextGenerationPipeline
from typing import List, Dict, Any

class HuggingFacePipeline:
    def __init__(self, model_name: str, tokenizer, model, **kwargs):
        self.model_name = model_name
        self.tokenizer = tokenizer
        self.model = model
        self.kwargs = kwargs

    def prompt_text_generation(self, prompt: str) -> str:
        generator = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer, return_full_text=False)
        response = generator(prompt, **self.kwargs)[0]['generated_text']
        return response

    def prompt_summarization(self, prompt: str) -> str:
        summarizer = pipeline("summarization", model=self.model, tokenizer=self.tokenizer, return_full_text=False)
        response = summarizer(prompt, **self.kwargs)[0]['summary_text']
        return response

    def prompt_question_answering(self, question: str, context: str) -> str:
        qa_pipeline = pipeline('question-answering', model=self.model, tokenizer=self.tokenizer, return_full_text=False)
        response = qa_pipeline(question=question, context=context, **self.kwargs)[0]['answer']
        return response

    def prompt_text2text_generation(self, prompt: str) -> str:
        text2text_generator = pipeline('text2text-generation', model=self.model, tokenizer=self.tokenizer, return_full_text=False)
        response = text2text_generator(prompt, **self.kwargs)[0]['generated_text']
        return response

    def prompt_table_question_answering(self, query: str, table: Dict[str, List[Any]]) -> str:
        table_qa_pipeline = pipeline('table-question-answering', model=self.model, tokenizer=self.tokenizer, return_full_text=False)
        response = table_qa_pipeline(query=query, table=table, **self.kwargs)[0]['answer']
        return response

    def prompt_text_classification(self, text: str) -> str:
        text_classifier = pipeline('text-classification', model=self.model, tokenizer=self.tokenizer, return_full_text=False)
        response = text_classifier(text, **self.kwargs)[0]['label']
        return response
