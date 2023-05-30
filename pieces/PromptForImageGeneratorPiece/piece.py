from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import openai

class PromptForImageGeneratorPiece(BasePiece):
    def openai_response(self, input_model: InputModel, prompt: str):
        # Input arguments
        openai_model = input_model.openai_model
        completion_max_tokens = input_model.completion_max_tokens
        temperature = input_model.temperature

        try:
            if openai_model in ["gpt-3.5-turbo", "gpt-4"]:
                response = openai.ChatCompletion.create(
                    model=openai_model,
                    messages = [
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=completion_max_tokens,
                )
                return response['choices'][0]['message']['content']
            else:
                response = openai.Completion.create(
                    model=openai_model,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=completion_max_tokens,
                )
                r_dict = response.to_dict_recursive()
                return r_dict["choices"][0]["text"]
        except Exception as e:
            self.logger.info(f"\nCompletion task failed: {e}")
            raise Exception(f"Completion task failed: {e}")

    def piece_function(self, input_model: InputModel):
        if self.secrets.OPENAI_API_KEY is None:
            raise Exception("OPENAI_API_KEY not found in ENV vars. Please add it to the secrets section of the Piece.")
        openai.api_key = self.secrets.OPENAI_API_KEY

        template = """You have access to an AI that generates images through text prompts. 
Your function is to write a prompt for this AI from a given context. 
Keep in mind that the AI generating images has no knowledge of the context you've been given. Therefore, it's crucial to include all the important information in the prompt you generate.
You  always write a short prompt that is designed to help the image generator AI create an image for the given context. 
You are very good at writing these text prompts for any context that is given  to you. 
You're very creative in how you describe the context you've been given, and like to vary the mood that runs through the prompt you've written. 
You always suggest some specific art style for the AI to create the image.
For this one the art style would be: {art_style}
Now, create a prompt to help the image generator AI to create an image for this context:
{context}"""

        prompt = template.format(art_style=input_model.art_style, context=input_model.context)
        self.logger.info(f"Generating prompt")
        generated_prompt = self.openai_response(input_model, prompt)

        if input_model.output_type == "string":
            self.logger.info("Returning prompt as a string")
            self.format_display_result(input_model, generated_prompt)
            return OutputModel(
                generated_prompt_string=generated_prompt,
            )
        
        output_file_path = f"{self.results_path}/generated_prompt.txt"
        with open(output_file_path, "w") as f:
            f.write(generated_prompt)

        if input_model.output_type == "file":
            self.logger.info(f"Prompt file saved at: {output_file_path}")
            self.format_display_result(input_model, generated_prompt)
            return OutputModel(
                generated_prompt_file_path=output_file_path
            )
        
        self.logger.info(f"Returning prompt as a string and file in: {output_file_path}")
        self.format_display_result(input_model, generated_prompt)
        return OutputModel(
            generated_prompt_string=generated_prompt,
            generated_prompt_file_path=output_file_path
        )
    
    def format_display_result(self, input_model: InputModel, generated_prompt_string: str):
        md_text = f"""
## Generated prompt:
{generated_prompt_string}

## Args
**context**: {input_model.context}
**model**: {input_model.openai_model}
**temperature**: {input_model.temperature}
**completion_max_tokens**: {input_model.completion_max_tokens}
"""
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }