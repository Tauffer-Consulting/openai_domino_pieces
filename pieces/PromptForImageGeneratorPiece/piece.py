from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import openai

class PromptForImageGeneratorPiece(BasePiece):
    def openai_chat_completion(self, input_model: InputModel, prompt: str, temperature: float = None):
        response = openai.ChatCompletion.create(
            model = input_model.openai_model,
            messages = [
                {"role": "user", "content": prompt}
            ],
            temperature = input_model.temperature if temperature is None else temperature,
            max_tokens = input_model.completion_max_tokens,
        )

        return response['choices'][0]['message']['content']

    def piece_function(self, input_model: InputModel):
        template = """You have access to an AI that generates images through text prompts. 
Your function is to write a prompt for this AI from a given context. 
You  always write a short prompt that is designed to help the image generator AI create an image for the given context. 
You are very good at writing these text prompts for any context that is given  to you. 
You're very creative in how you describe the context you've been given, and like to vary the mood that runs through the prompt you've written. 
It also always suggests some specific art style for the AI to create the image.
For this one the art style would be: {art_style}
Now, create a prompt to help the image generator AI to create an image for this context:
{context}"""

        openai.api_key = self.secrets.OPENAI_API_KEY
        prompt = template.format(art_style=input_model.art_style, context=input_model.context)
        generated_prompt = self.openai_chat_completion(input_model, prompt)

        if not input_model.output_file_name:
            return OutputModel(
                generated_prompt_string=generated_prompt,
            )
        
        output_file_path = f"{self.results_path}/{input_model.output_file_name}.txt"
        with open(output_file_path, "w") as f:
            f.write(generated_prompt)
        
        self.logger.info(f"Prompt file saved at: {output_file_path}")
    
        return OutputModel(
            generated_prompt_string=generated_prompt,
            generated_prompt_file_path=output_file_path
        )