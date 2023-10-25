from pydantic import BaseModel, Field
from enum import Enum


class ImageSize(str, Enum):
    """
    Image size to generate
    """
    high_quality = "1024x1024"
    medium_quality = "512x512"
    low_quality = "256x256"


class ImageFormat(str, Enum):
    """
    Image format to return
    """
    url = "url"
    image_png = "image_png"
    base64_string = "base64_string"


class OutputTypeType(str, Enum):
    """
    Output type for the result text
    """
    file = "file"
    string = "string"
    file_and_string = "file_and_string"


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
    image_format: ImageFormat = Field(
        default=ImageFormat.url,
        description="The format in which the generated image is returned",
        
    )
    output_type: OutputTypeType = Field(
        default=OutputTypeType.string,
        description='The type of the output. Attention: if Response Format equals to image_png, then Output Type must be file type.',
        
    )


class OutputModel(BaseModel):
    """
    ImageGeneratorPiece output model
    """
    output_string: str = Field(
        default=None,
        description="The generated image as string",
    )
    output_file_path: str = Field(
        default=None,
        description="Path to the generated image",
    )


class SecretsModel(BaseModel):
    """
    ImageGeneratorPiece secrets model
    """
    OPENAI_API_KEY: str = Field(
        description="Your OpenAI API key"
    )