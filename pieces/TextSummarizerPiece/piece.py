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
            model = input_model.openai_model_name,
            messages = [
                {"role": "user", "content": text}
            ],
            temperature = input_model.temperature,
            max_tokens = input_model.max_tokens,
        )

        return response['choices'][0]['message']['content']
    
    async def agenerate_chat_completion(self, input_model: InputModel, texts_chunks: List):
        tasks = [self.chat_completion_method(input_model, text) for text in texts_chunks]
        return await asyncio.gather(*tasks)
    
    def piece_function(self, input_model: InputModel):        
        encoding = tiktoken.encoding_for_model(input_model.openai_model_name)
        len_chunk_text = input_model.chunk_size - len(encoding.encode(text=self.prompt))
        full_text_tokens = encoding.encode(text=input_model.text)
        texts_chunks_with_prompt = []
        for i in range(0, len(full_text_tokens), len_chunk_text):
            idx_chunk_start = [i - input_model.chunk_overlap if i>0 else 0][0]
            decoded_text_chunk = encoding.decode(full_text_tokens[idx_chunk_start:i+len_chunk_text])
            text_chunk_with_prompt = self.prompt.format(text=decoded_text_chunk) 
            texts_chunks_with_prompt.append(text_chunk_with_prompt)
        
        openai.api_key = self.secrets.OPENAI_API_KEY
        
        loop = asyncio.new_event_loop()
        summaries_chunks = loop.run_until_complete(self.agenerate_chat_completion(input_model, texts_chunks_with_prompt))
        joined_summaries_chunks = [" ".join(summaries_chunks)]
        final_summary = loop.run_until_complete(self.agenerate_chat_completion(input_model, joined_summaries_chunks))

        return OutputModel(
            summarized_text = final_summary
        )

