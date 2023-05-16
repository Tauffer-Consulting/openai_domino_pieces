from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import openai

class TextGeneratorPiece(BasePiece):    
    def openai_chat_completion(self, openai_model:str, prompt: str, temperature: float, completion_max_tokens: int):
        response = openai.ChatCompletion.create(
            model = openai_model,
            messages = [
                {"role": "user", "content": prompt}
            ],
            temperature = temperature,
            max_tokens = completion_max_tokens,
        )

        return response['choices'][0]['message']['content']
        
    def piece_function(self, input_model: InputModel):
        openai.api_key = self.secrets.OPENAI_API_KEY
        template = input_model.template
        # params = input_model.prompt_params
        prompt_args = input_model.prompt_args
        dict_args = {}
        for arg in prompt_args:
            dict_args[arg.arg_name] = arg.arg_value
        # prompt = template.format(**params)
        prompt = template.format(**dict_args)
        response = self.openai_chat_completion(input_model.openai_model, prompt, input_model.temperature, input_model.completion_max_tokens)

        return OutputModel(
            generated_text=response,
        )