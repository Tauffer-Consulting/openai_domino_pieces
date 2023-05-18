from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from typing import List
from enum import Enum
import openai
import tiktoken
import asyncio


class TokenLimit(int, Enum):
    gpt_3_5_turbo = 4000
    gpt_4 = 8000
    ada = 2000
    babbage = 2000
    curie = 2000
    davinci = 2000
class TextSummarizerPiece(BasePiece):  

    async def chat_completion_method(self, input_model: InputModel, prompt: str):
        self.logger.info("Running OpenAI completion request...")
        try:
            if input_model.openai_model in ["gpt-3.5-turbo", "gpt-4"]:
                response = openai.ChatCompletion.create(
                    model = input_model.openai_model,
                    messages = [
                        {"role": "user", "content": prompt}
                    ],
                    temperature = input_model.temperature,
                    max_tokens = input_model.completion_max_tokens,
                )
                string_generated_text = response['choices'][0]['message']['content']
            else:
                response = openai.Completion.create(
                    model = input_model.openai_model,
                    prompt = prompt,
                    temperature = input_model.temperature,
                    max_tokens = input_model.completion_max_tokens,
                )
                r_dict = response.to_dict_recursive()
                string_generated_text = r_dict["choices"][0]["text"]
        except Exception as e:
            self.logger.info(f"\nCompletion task failed: {e}")
            raise Exception(f"Completion task failed: {e}")
        return string_generated_text
    
    async def agenerate_chat_completion(self, input_model: InputModel, texts_chunks: List):
        tasks = [self.chat_completion_method(input_model=input_model, prompt=text) for text in texts_chunks]
        return await asyncio.gather(*tasks)
    
    def create_chunks_with_prompt(self, input_model: InputModel, text: str):
        text_chunk_size = input_model.chunk_size - len(self.encoding.encode(text=self.prompt))
        total_text_tokens = self.encoding.encode(text=text)
        chunk_overlap = round(input_model.chunk_overlap_rate * text_chunk_size)
        text_chunks_with_prompt = []
        for i in range(0, len(total_text_tokens), text_chunk_size):
            idx_chunk_start = [i - chunk_overlap if i>0 else 0][0]
            decoded_text_chunk = self.encoding.decode(total_text_tokens[idx_chunk_start:i+text_chunk_size])
            chunk_with_prompt = self.prompt.format(text=decoded_text_chunk) 
            text_chunks_with_prompt.append(chunk_with_prompt)
        return text_chunks_with_prompt
    
    def format_display_result(self, input_model: InputModel, final_summary: str):
        md_text = f"""
## Summarized text
{final_summary}

## Args
**model**: {input_model.openai_model}
**temperature**: {input_model.temperature}
**max_tokens**: {input_model.completion_max_tokens}

"""
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }
        
    def piece_function(self, input_model: InputModel):                
        # OpenAI settings
        if self.secrets.OPENAI_API_KEY is None:
            raise Exception("OPENAI_API_KEY not found in ENV vars. Please add it to the secrets section of the Piece.")
        openai.api_key = self.secrets.OPENAI_API_KEY

        # Input arguments
        token_limits = TokenLimit[input_model.openai_model.name].value
        completion_max_tokens = input_model.completion_max_tokens
        text_token_count = token_limits
        if input_model.text_file_path:
             with open(input_model.text_file_path, "r") as f:
                text = f.read()
        else: 
            text = input_model.text

        self.prompt = """Write a concise summary of the text below, while maintaining its original writing form.
---        
text:
    
{text}
---
concise summary:"""

        # Summarizing loop
        loop = asyncio.new_event_loop()
        self.encoding = tiktoken.encoding_for_model(input_model.openai_model)
        self.logger.info(f"Loading text")
        while text_token_count > (token_limits - completion_max_tokens):
            texts_chunks_with_prompt = self.create_chunks_with_prompt(input_model=input_model, text=text)
            summaries_chunks = loop.run_until_complete(self.agenerate_chat_completion(input_model, texts_chunks_with_prompt))
            text = " ".join(summaries_chunks)
            text_token_count = len(self.encoding.encode(text=text))

        self.logger.info(f"Summarizing text")
        response = loop.run_until_complete(self.agenerate_chat_completion(input_model, [text]))
        final_summary = response[0]

        # Display result in the Domino GUI
        self.format_display_result(input_model,final_summary)

        if input_model.output_type == "string":
            self.logger.info(f"Returning final summary as a string")
            return OutputModel(
                string_summarized_text=final_summary,
            )
        
        output_file_path = f"{self.results_path}/{input_model.output_file_name}"
        with open(output_file_path, "w") as f:
                f.write(final_summary)
        
        if input_model.output_type == "file":
            self.logger.info(f"Saved final summary as file in {output_file_path}")
            return OutputModel(
                file_path_summarized_text=output_file_path
            )
        
        self.logger.info(f"Returning final summary as a string and file in: {output_file_path}")
        return OutputModel(
            string_summarized_text=final_summary,
            file_path_summarized_text=output_file_path
        )

