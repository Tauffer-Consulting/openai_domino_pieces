from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import os
import openai


class CompletionsPiece(BasePiece):
    """
    This Piece uses the OpenAI API to generate text completions.
    """
    
    def piece_function(self, input_model: InputModel):

        # Secrets are retrieved from ENV vars
        openai_api_key = os.environ.get("OPENAI_API_KEY", None)
        if openai_api_key is None:
            raise Exception("OPENAI_API_KEY not found in ENV vars. Please add it to the secrets section of the Piece.")
        openai.api_key = openai_api_key

        # Input arguments are retrieved from the Input model object
        llm_model_name = input_model.llm_model_name
        prompt = input_model.prompt
        max_tokens = input_model.max_tokens
        temperature = input_model.temperature

        print("Making OpenAI completion request...")
        try:
            r = openai.Completion.create(
                model=llm_model_name,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            r_dict = r.to_dict_recursive()
            result_text = r_dict["choices"][0]["text"]
            usage_total_tokens = r_dict["usage"]["total_tokens"]
            message = "\nCompletion task was successful!"
        except Exception as e:
            print(f"\nCompletion task failed: {e}")
            raise Exception(f"Completion task failed: {e}")

        # Finally, results should return as an Output model
        return OutputModel(
            message=message,
            result_text=result_text,
            usage_total_tokens=usage_total_tokens
        )