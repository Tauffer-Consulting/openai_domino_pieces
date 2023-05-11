from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import openai
import base64

class ImageGeneratorPiece(BasePiece):
    def piece_function(self, input_model: InputModel):
        openai.api_key = self.secrets.OPENAI_API_KEY
        response = openai.Image.create(
            prompt=input_model.prompt,
            n=1,
            size=input_model.size,
            response_format=input_model.response_format,
        )
    
        image_data =  response['data'][0][input_model.response_format]
        
        if input_model.response_format == "b64_json":
            image = base64.b64decode(image_data)
            output_file_path = f"{self.results_path}/{input_model.output_file_name}.png"
            open_mode = "wb"
        else:
            image = image_data
            output_file_path = f"{self.results_path}/{input_model.output_file_name}.txt"
            open_mode = "w"

        with open(output_file_path, open_mode) as f:
            f.write(image)
        
        return OutputModel(
            output_file_path=output_file_path,
        )