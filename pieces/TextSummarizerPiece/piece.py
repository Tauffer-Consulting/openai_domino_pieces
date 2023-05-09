from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from typing import List
import openai
import tiktoken
import asyncio


class TextSummarizerPiece(BasePiece):
    
    prompt = """Write a summary of the given text while maintaining its original writing form.

text:
    
{text}

CONCISE SUMMARY:"""
    
    async def chat_completion_method(self, input_model: InputModel, text: str):
        response = openai.ChatCompletion.create(
            model = input_model.openai_model,
            messages = [
                {"role": "user", "content": text}
            ],
            temperature = input_model.temperature,
            max_tokens = input_model.completion_max_tokens,
        )

        return response['choices'][0]['message']['content']
    
    async def agenerate_chat_completion(self, input_model: InputModel, texts_chunks: List):
        tasks = [self.chat_completion_method(input_model, text) for text in texts_chunks]
        return await asyncio.gather(*tasks)
    
    def create_chunks_with_prompt(self, input_model: InputModel, text: str):
        encoding = tiktoken.encoding_for_model(input_model.openai_model)
        text_chunk_size = input_model.chunk_size - len(encoding.encode(text=self.prompt))
        total_text_tokens = encoding.encode(text=text)
        chunk_overlap = round(input_model.chunk_overlap_rate * text_chunk_size)
        text_chunks_with_prompt = []
        for i in range(0, len(total_text_tokens), text_chunk_size):
            idx_chunk_start = [i - chunk_overlap if i>0 else 0][0]
            decoded_text_chunk = encoding.decode(total_text_tokens[idx_chunk_start:i+text_chunk_size])
            chunk_with_prompt = self.prompt.format(text=decoded_text_chunk) 
            text_chunks_with_prompt.append(chunk_with_prompt)
        return text_chunks_with_prompt
        
    
    def piece_function(self, input_model: InputModel):                
        openai.api_key = self.secrets.OPENAI_API_KEY
        loop = asyncio.new_event_loop()

        encoding = tiktoken.encoding_for_model(input_model.openai_model)
        token_limits = (4000 if input_model.openai_model == "gpt-3.5-turbo" else 8000)
        completion_max_tokens = input_model.completion_max_tokens
        text_token_count = token_limits
        if input_model.text_file_path:
             with open(input_model.text_file_path, "r") as f:
                text = f.read()
        else: text = input_model.text
        while text_token_count > (token_limits - completion_max_tokens):
            texts_chunks_with_prompt = self.create_chunks_with_prompt(input_model=input_model, text=text)
            summaries_chunks = loop.run_until_complete(self.agenerate_chat_completion(input_model, texts_chunks_with_prompt))
            text = " ".join(summaries_chunks)
            text_token_count = len(encoding.encode(text=text))

        final_summary = loop.run_until_complete(self.agenerate_chat_completion(input_model, [text]))
        
        output_file_path = f"{self.results_path}/{input_model.output_file_name}"
        with open(output_file_path, "w") as f:
                f.write(final_summary[0])

        return OutputModel(
            summarized_text=final_summary[0],
            summarized_text_file_path=output_file_path
        )

