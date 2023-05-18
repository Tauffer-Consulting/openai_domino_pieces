from pydantic import BaseModel, Field, FilePath
from enum import Enum


class ImageSize(str, Enum):
    """
    Image size to generate
    """
    high_quality = "1024x1024"
    medium_quality = "512x512"
    low_quality = "256x256"


class ResponseFormat(str, Enum):
    """
    Response format to return
    """
    url = "url"
    image_png = "image_png"
    base64_string = "base64_string"


class InputModel(BaseModel):
    """
    ImageGeneratorPiece input model
    """
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
    """
    ImageGeneratorPiece output model
    """
    output_file_path: FilePath = Field(
        description="Path to the generated image",
    )


class SecretsModel(BaseModel):
    """
    ImageGeneratorPiece secrets model
    """
    OPENAI_API_KEY: str = Field(
        description="Your OpenAI API key"
    )