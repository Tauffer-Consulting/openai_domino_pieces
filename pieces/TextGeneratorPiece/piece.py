from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import openai


class TextGeneratorPiece(BasePiece):   
        
    def piece_function(self, input_model: InputModel):
        # OpenAI settings
        if self.secrets.OPENAI_API_KEY is None:
            raise Exception("OPENAI_API_KEY not found in ENV vars. Please add it to the secrets section of the Piece.")
        openai.api_key = self.secrets.OPENAI_API_KEY

        # Input arguments
        openai_model = input_model.openai_model
        completion_max_tokens = input_model.completion_max_tokens
        temperature = input_model.temperature
        template = input_model.template
        dict_args = {}
        for arg in input_model.prompt_args:
            dict_args[arg.arg_name] = arg.arg_value
        prompt = template.format(**dict_args)

        # Generate text based on prompt
        self.logger.info("Running OpenAI completion request...")
        try:
            if openai_model in ["gpt-3.5-turbo", "gpt-4"]:
                response = openai.ChatCompletion.create(
                    model = openai_model,
                    messages = [
                        {"role": "user", "content": prompt}
                    ],
                    temperature = temperature,
                    max_tokens = completion_max_tokens,
                )
                string_generated_text = response['choices'][0]['message']['content']
            else:
                response = openai.Completion.create(
                    model = openai_model,
                    prompt = prompt,
                    temperature = temperature,
                    max_tokens = completion_max_tokens,
                )
                r_dict = response.to_dict_recursive()
                string_generated_text = r_dict["choices"][0]["text"]
        except Exception as e:
            self.logger.info(f"\nCompletion task failed: {e}")
            raise Exception(f"Completion task failed: {e}")
        
        # Display result in the Domino GUI
        self.format_display_result(input_model,string_generated_text, prompt)

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
    
    def format_display_result(self, input_model: InputModel, string_generated_text: str, prompt: str):
        md_text = f"""
## Generated text
{string_generated_text}

## Args
**prompt**: {prompt}
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