from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import openai

class TextSummarizerPiece(BasePiece):
    def piece_function(self, input_model: InputModel):
        prompt = input_model.prompt_template.format(text=input_model.text)
        openai.api_key = self.secrets.OPENAI_API_KEY
        
        response = openai.ChatCompletion.create(
            model = input_model.openai_model_name,
            messages = [
                {"role": "user", "content": prompt}
            ],
            temperature = input_model.temperature,
            max_tokens = input_model.max_tokens,
        )            

        return OutputModel(
            summarized_text = response['choices'][0]['message']['content']
        )

