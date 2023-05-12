from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from enum import Enum
import openai
import base64

class ResponseFormatArray(Enum):
    url = {"user_value":"url", "api_value": "url", "file_extension": ".txt"}
    base64_string = {"user_value":"base64_string", "api_value": "b64_json", "file_extension":  ".txt"}
    image_png = {"user_value":"image_png", "api_value": "b64_json", "file_extension": ".png"}
class ImageGeneratorPiece(BasePiece):
    def piece_function(self, input_model: InputModel):
        openai.api_key = self.secrets.OPENAI_API_KEY
        response_format = ResponseFormatArray[input_model.response_format].value

        self.logger.info(f"Generating image with prompt: {input_model.prompt}")
        response = openai.Image.create(
            prompt=input_model.prompt,
            n=1,
            size=input_model.size,
            response_format=response_format["api_value"],
        )
    
        image_data =  response['data'][0][response_format["api_value"]]
        

        if response_format["user_value"] == "image_png":
            image = base64.b64decode(image_data)
            open_mode = "wb"
        else: 
            image = image_data
            open_mode = "w"
        
        format_extension = response_format["file_extension"]
        output_file_path = f"{self.results_path}/{input_model.output_file_name}{format_extension}"

        with open(output_file_path, open_mode) as f:
            f.write(image)
        
        self.logger.info(f"Image saved at: {output_file_path}")
        
        return OutputModel(
            output_file_path=output_file_path,
        )