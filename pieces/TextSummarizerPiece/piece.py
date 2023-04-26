from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import openai

class TextSummarizerPiece(BasePiece):
    def piece_function(self, input_model: InputModel):
        prompt_template=f"""Write a summary of the given text while maintaining its original writing form, whether it is in the first, second, or third person.

text:
    
"{input_model.text}"

CONCISE SUMMARY:"""

        openai.api_key = self.secrets.OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model = input_model.openai_model_name,
            messages = [
                {"role": "user", "content": prompt_template}
            ],
            temperature = 0.3
        )

        return OutputModel(
            summarized_text = response['choices'][0]['message']['content']
        )

