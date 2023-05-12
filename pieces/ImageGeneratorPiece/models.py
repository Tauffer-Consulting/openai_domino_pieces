from pydantic import BaseModel, Field
from enum import Enum

class ImageSize(str, Enum):
    high_quality = "1024x1024"
    medium_quality = "512x512"
    low_quality = "256x256"

class ResponseFormat(str, Enum):
    url = "url"
    image_png = "image_png"
    base64_string = "base64_string"

class InputModel(BaseModel):
    """MyNewPiece Input"""
    prompt: str = Field(
        ...,
        description="A text description of the desired image",
    )

    size: ImageSize = Field(
        default=ImageSize.high_quality,
        description="The size of the generated images",
    )

    response_format: ResponseFormat = Field(
        default=ResponseFormat.url,
        description="The format in which the generated image is returned"
    )

    output_file_name: str = Field(
        default="generated_image",
        description="The name of the generated image, without the extension format"
    )

class OutputModel(BaseModel):
    """MyNewPiece Output"""
    output_file_path: str = Field(
        description="Path to the generated image",
    )

class SecretsModel(BaseModel):
    """MyNewPiece Secrets"""
    
    OPENAI_API_KEY: str = Field(
        description="Your OpenAI API key"
    )