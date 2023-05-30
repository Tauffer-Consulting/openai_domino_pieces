from pydantic import BaseModel, Field, FilePath
from enum import Enum
from typing import Union


class OutputTypeType(str, Enum):
    """
    Output type for the result text
    """
    file = "file"
    string = "string"
    file_and_string = "file_and_string"


class InputModel(BaseModel):
    """
    AudioTranscriptPiece input model
    """
    audio_file_path: FilePath = Field(
        ...,
        description='The path to the audio file to process.',
    )
    output_type: OutputTypeType = Field(
        default=OutputTypeType.string,
        description='The type of output for the result text'
    )
    temperature: float = Field(
        description="What sampling temperature to use, between 0 and 1",
        default=0.1,
        gt=0.,
        le=1
    )


class OutputModel(BaseModel):
    """
    AudioTranscriptPiece output model
    """
    message: str = Field(
        description="Output message to log"
    )
    string_transcription_result: str = Field(
        default=None,
        description="The result transcription text as a string."
    )
    file_path_transcription_result: FilePath = Field(
        default=None,
        description="The result transcription text as a file path."
    )


class SecretsModel(BaseModel):
    """
    AudioTranscriptPiece secret model
    """
    OPENAI_API_KEY: str = Field(
        description="OpenAI API key"
    )