from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from enum import Enum
import openai
import base64


class ImageGeneratorPiece(BasePiece):
    def piece_function(self, input_model: InputModel):
        if self.secrets.OPENAI_API_KEY is None:
            raise Exception("OPENAI_API_KEY not found in ENV vars. Please add it to the secrets section of the Piece.")
        openai.api_key = self.secrets.OPENAI_API_KEY
        
        response_format = input_model.image_format if input_model.image_format == "url" else "b64_json"
        self.logger.info(f"Generating image with prompt: {input_model.prompt}")
        try:
            response = openai.Image.create(
                prompt=input_model.prompt,
                n=1,
                size=input_model.size,
                response_format=response_format,
            )
            image_data =  response['data'][0][response_format]
        except Exception as e:
            self.logger.info(f"\nImage generation failed: {e}")
            raise Exception(f"Image generation failed: {e}")
        
        if input_model.output_type == "string":
            if input_model.image_format == "image_png":
                self.logger.info(f"PNG Image format can not be returned as a string. Returning it as a png file")
            else:
                # Display result in the Domino GUI
                self.format_display_result(image_format=input_model.image_format, image_data=image_data)
                self.logger.info(f"Returning image as a string")
                return OutputModel(
                    output_string=str(image_data)
                )        

        # Define variables to save image to file
        if input_model.image_format == "image_png":
            image = base64.b64decode(image_data)
            file_type = "png"
            open_mode = "wb"
        else: 
            image = image_data
            file_type = "txt"
            open_mode = "w"

        #Save image to file
        output_file_path = f"{self.results_path}/{input_model.output_file_name}.{file_type}"
        with open(output_file_path, open_mode) as f:
            f.write(image)

        if input_model.output_type == "file_and_string":
            if input_model.image_format == "image_png":
                self.logger.info(f"PNG Image format can not be returned as a string. Returning it as a png file.")
            else:
                # Display result in the Domino GUI
                self.format_display_result(image_format=input_model.image_format, image_data=image_data)
                self.logger.info(f"Returning image as a string and file at {output_file_path}")
                return OutputModel(
                    output_string=str(image_data),
                    output_file_path=output_file_path,
                )

        # Display result in the Domino GUI
        self.format_display_result(image_format=input_model.image_format, image_data=image_data)
        self.logger.info(f"Returning image as a file at {output_file_path}")
        return OutputModel(
            output_file_path=output_file_path,
        )
    
    def format_display_result(self, image_format: str, image_data: str):
        if image_format == "image_png":
            self.display_result = {
                "file_type": "png",
                "base64_content": image_data,
                # "file_path": ""
            }
            return

        md_text = """
Image generated as {image_format}.  \n 
"""
        if image_format == "url":
            final_md_text = md_text.format(image_format="URL")
            final_md_text += f"Image URL: [{image_data}]({image_data})"
        if image_format == "base64_string":
            final_md_text = md_text.format(image_format="Base64 String")
            final_md_text += "Base64 String too long to be displayed."

        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(final_md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }