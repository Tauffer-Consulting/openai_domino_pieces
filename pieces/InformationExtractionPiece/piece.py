from domino.base_piece import BasePiece
from .models import InputModel, OutputModel, SecretsModel
from openai import OpenAI
import json
from typing import Union


class InformationExtractionPiece(BasePiece):

    def piece_function(self, input_data: InputModel, secrets_data: SecretsModel):
        # OpenAI settings
        if secrets_data.OPENAI_API_KEY is None:
            raise Exception("OPENAI_API_KEY not found in ENV vars. Please add it to the secrets section of the Piece.")

        client = OpenAI(api_key=secrets_data.OPENAI_API_KEY)
        prompt = f"""Extract the following information from the text below as JSON.
The output can be a simple json or a list of jsons but never a nested json.
Use the items to be extract as information to identify the right information to be extract:
---
Input text: {input_data.input_text}
Items to be extracted:
{input_data.extract_items}
"""
        response = client.chat.completions.create(
            response_format={
                "type": "json_object"
            },
            temperature=0,
            model=input_data.openai_model,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        if not response.choices:
            raise Exception("No response from OpenAI")

        if response.choices[0].message.content is None:
            raise Exception("No response from OpenAI")

        output_json = json.loads(response.choices[0].message.content)
        if not all(item.name in output_json for item in input_data.extract_items):
            key = list(output_json.keys())[0]
            if isinstance(output_json[key], list):
                output_json = output_json[key]

        # Return extracted information
        self.logger.info("Returning extracted information")
        if isinstance(output_json, dict):
            self.format_display_result_object(input_data, output_json)
            return OutputModel(**output_json, output_data=json.dumps(output_json))

        self.format_display_result_table(input_data, output_json)
        return OutputModel(output_data=json.dumps(output_json))

    def format_display_result_object(self, input_data: InputModel, result: dict):
        md_text = """## Extracted Information\n"""

        for item in input_data.extract_items:
            md_text += f"""### {item.name}:\n{result.get(item.name)}\n"""
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }

    def format_display_result_table(self, input_data: InputModel, result: Union[dict, list]):
        # Headers from extract_items
        headers = [item.name for item in input_data.extract_items]
        md_text = "## Extracted Information\n\n"

        if isinstance(result, list):
            # Generate table headers
            md_text += "| " + " | ".join(headers) + " |\n"
            md_text += "|---" * len(headers) + "|\n"

            # Populate table rows
            for res in result:
                row = [
                    str(res.get(item.name))
                    for item in input_data.extract_items
                ]
                md_text += "| " + " | ".join(row) + " |\n"
        else:
            # Single object case
            md_text += "| " + " | ".join(headers) + " |\n"
            md_text += "|---" * len(headers) + "|\n"
            row = [
                str(result.get(item.name))
                for item in input_data.extract_items
            ]
            md_text += "| " + " | ".join(row) + " |\n"

        self.logger.info(md_text)
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }
