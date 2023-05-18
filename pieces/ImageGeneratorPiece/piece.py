from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from enum import Enum
import openai
import base64


class ResponseFormatArray(Enum):
    url = {"user_value":"url", "api_value": "url", "file_type": ".txt"}
    base64_string = {"user_value":"base64_string", "api_value": "b64_json", "file_type":  ".txt"}
    image_png = {"user_value":"image_png", "api_value": "b64_json", "file_type": ".png"}


class ImageGeneratorPiece(BasePiece):
    def piece_function(self, input_model: InputModel):
        if self.secrets.OPENAI_API_KEY is None:
            raise Exception("OPENAI_API_KEY not found in ENV vars. Please add it to the secrets section of the Piece.")
        openai.api_key = self.secrets.OPENAI_API_KEY
        response_format = ResponseFormatArray[input_model.response_format].value

        self.logger.info(f"Generating image with prompt: {input_model.prompt}")
        try:
            response = openai.Image.create(
                prompt=input_model.prompt,
                n=1,
                size=input_model.size,
                response_format=response_format["api_value"],
            )
            image_data =  response['data'][0][response_format["api_value"]]
        except Exception as e:
            self.logger.info(f"\nImage generation failed: {e}")
            raise Exception(f"Image generation failed: {e}")

        if response_format["user_value"] == "image_png":
            image = base64.b64decode(image_data)
            open_mode = "wb"
        else: 
            image = image_data
            open_mode = "w"
        
        file_type = response_format["file_type"]
        output_file_path = f"{self.results_path}/{input_model.output_file_name}{file_type}"

        with open(output_file_path, open_mode) as f:
            f.write(image)
        
        self.logger.info(f"Image saved at: {output_file_path}")

        self.format_display_result(file_type=file_type, output_file_path=output_file_path)
        
        return OutputModel(
            output_file_path=output_file_path,
        )
    
    def format_display_result(self, file_type: str, output_file_path: str):
        if file_type == "png":
            self.display_result = {
                "file_type": "png",
                "file_path": output_file_path
            }
        else:
            self.display_result = {
                "file_type": "txt",
                "file_path": output_file_path
            }