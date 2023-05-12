from pydantic import BaseModel, Field, FilePath
from enum import Enum
from typing import Union

class OutputTypeType(str, Enum):
    """
    Output type for the result text
    """

    string = "string"
    file = "file"


class InputModel(BaseModel):
    """
    Audio Transcript input model
    """

    audio_file_path: str = Field(
        ...,
        description='The path to the audio file to process.',
    )
    output_type: OutputTypeType = Field(
        default=OutputTypeType.string,
        description='The type of output fot the result text'
    )
    temperature: float = Field(
        description="What sampling temperature to use, between 0 and 1",
        default=0.1,
        gt=0.,
        le=1
    )


class OutputModel(BaseModel):
    """
    Audio Transcript output model
    """

    message: str = Field(
        description="Output message to log"
    )
    transcription_result: Union[str, FilePath] = Field(
        description="The result transcription text."
    )


class SecretsModel(BaseModel):
    """
    Audio Transcript secret model
    """
    
    OPENAI_API_KEY: str = Field(
        description="OpenAI API key"
    )