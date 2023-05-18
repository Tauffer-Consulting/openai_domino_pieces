from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import openai


class TextGeneratorPiece(BasePiece):   
        
    def piece_function(self, input_model: InputModel):
        # OpenAI settings
        openai.api_key = self.secrets.OPENAI_API_KEY
        template = input_model.template
        dict_args = {}
        for arg in input_model.prompt_args:
            dict_args[arg.arg_name] = arg.arg_value
        prompt = template.format(**dict_args)

        # Generate text based on prompt
        self.logger.info("Generating text...")
        response = openai.ChatCompletion.create(
            model = input_model.openai_model,
            messages = [
                {"role": "user", "content": prompt}
            ],
            temperature = input_model.temperature,
            max_tokens = input_model.completion_max_tokens,
        )
        string_generated_text = response['choices'][0]['message']['content']

        # Format output
        self.logger.info("Text generated!")
        if input_model.output_type == "string":
            self.logger.info("Returning generated text as a string")
            return OutputModel(
                string_generated_text=string_generated_text,
            )
        
        output_file_path = f"{self.results_path}/{input_model.output_file_name}"
        with open(output_file_path, "w") as f:
            f.write(string_generated_text)
        
        if input_model.output_type == "file":
            self.logger.info(f"Generated text saved at: {output_file_path}")
            return OutputModel(
                file_path_generated_text=output_file_path
            )

        self.logger.info(f"Returning generated text as string and file in {output_file_path}")
        return OutputModel(
            string_generated_text=string_generated_text,
            file_path_generated_text=output_file_path
        )