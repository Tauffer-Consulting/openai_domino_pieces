from domino.base_piece import BasePiece
from .models import InputModel, OutputModel, SecretsModel
from openai import OpenAI
import json
from typing import Union, Optional
import pickle


class FileInformationExtractionPiece(BasePiece):

    def piece_function(self, input_data: InputModel, secrets_data: SecretsModel):
        # OpenAI settings
        if secrets_data.OPENAI_API_KEY is None:
            raise Exception("OPENAI_API_KEY not found in ENV vars. Please add it to the secrets section of the Piece.")

        self.client = OpenAI(api_key=secrets_data.OPENAI_API_KEY)

        with open(input_data.input_file_path, "rb") as file:
            file_content = pickle.load(file)
        
        result = []

        if isinstance(file_content, dict):
            output_json = self.extract_json_infos(content=file_content, extract_items=input_data.extract_items, model=input_data.openai_model, additional_info=input_data.additional_information)
            result.append(output_json)
        elif isinstance(file_content, list):
            for i, item_content in enumerate(file_content):
                self.logger.info(f"Extract item i:{i}")
                output_json = self.extract_json_infos(content=item_content, extract_items=input_data.extract_items, model=input_data.openai_model,additional_info=input_data.additional_information)
                result.append(output_json)

        self.logger.info(result)

        # Return extracted information
        self.logger.info("Returning extracted information")

        self.format_display_result_table(input_data, result)
        return OutputModel(output_data=result)

    def extract_json_infos(self, content: dict, extract_items: dict, model: str, additional_info: Optional[str] = None):

        optional_additional_info = "" if not additional_info else f"You can use the following additional information to help filling the request items to be extracted. Additional information: {additional_info}."

        prompt = f"""Extract the following information from the text below as JSON.
The output can be a simple json or a list of jsons but never a nested json.
{optional_additional_info}
Use the items to be extract as information to identify the right information to be extract:
---
Input text: {content}
Items to be extracted:
{extract_items}

"""
        
        response = self.client.chat.completions.create(
            response_format={
                "type": "json_object"
            },
            temperature=0,
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        if not response.choices:
            raise Exception("No response from OpenAI")

        if response.choices[0].message.content is None:
            raise Exception("No response from OpenAI")
        
        return json.loads(response.choices[0].message.content)

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

        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }
