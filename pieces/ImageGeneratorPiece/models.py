from pydantic import BaseModel, Field
from enum import Enum

class ImageSize(str, Enum):
    high_quality = "1024x1024"
    medium_quality = "512x512"
    low_quality = "256x256"

class ResponseFormat(str, Enum):
    url = "url",
    b64_json = "b64_json"

class InputModel(BaseModel):
    """MyNewPiece Input"""
    prompt: str = Field(
        default=None,
        description="A text description of the desired image",
    )

    size: str = Field(
        default=ImageSize.high_quality,
        description="The size of the generated images",
    )

    response_format: str = Field(
        default=ResponseFormat.url,
        description="The format in which the generated images are returned"
    )

    output_file_name: str = Field(
        default="output_image",
        description="The name of the generated image, without the extension"
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