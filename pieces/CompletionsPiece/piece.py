from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import os
import openai


class CompletionsPiece(BasePiece):
    """
    This Piece uses the OpenAI API to generate text completions.
    """
    
    def piece_function(self, input_model: InputModel):
        openai_api_key = self.secrets.OPENAI_API_KEY
        if openai_api_key is None:
            raise Exception("OPENAI_API_KEY not found in ENV vars. Please add it to the secrets section of the Piece.")
        openai.api_key = openai_api_key

        # Input arguments are retrieved from the Input model object
        llm_model_name = input_model.llm_model_name
        max_tokens = input_model.max_tokens
        temperature = input_model.temperature

        if input_model.prompt_file_path:
            with open(input_model.prompt_file_path, "r") as f:
                prompt = f.read()
        else: prompt = input_model.prompt

        self.logger.info("Making OpenAI completion request...")
        try:
            r = openai.Completion.create(
                model=llm_model_name,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            r_dict = r.to_dict_recursive()
            completion_result = r_dict["choices"][0]["text"]
            usage_total_tokens = r_dict["usage"]["total_tokens"]
            message = "\nCompletion task was successful!"
        except Exception as e:
            self.logger.info(f"\nCompletion task failed: {e}")
            raise Exception(f"Completion task failed: {e}")
        
        if input_model.output_type == "string":
            return OutputModel(
                message=message,
                completion_result=completion_result,
                usage_total_tokens=usage_total_tokens
            )

        output_file_path = f"{self.results_path}/completion_result.txt"
        with open(output_file_path, "w") as f:
            f.write(completion_result)

        # Finally, results should return as an Output model
        return OutputModel(
            message=message,
            completion_result=output_file_path,
            usage_total_tokens=usage_total_tokens
        )