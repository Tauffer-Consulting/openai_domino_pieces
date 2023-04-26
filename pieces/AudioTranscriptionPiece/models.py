from pydantic import BaseModel, Field, FilePath
from enum import Enum


class OutputTypeType(str, Enum):
    xcom = "xcom"
    file = "file"


class InputModel(BaseModel):
    file_path: str = Field(
        description='The path to the text file to process.',
    )
    output_type: OutputTypeType = Field(
        description='The type of output fot the result text.',
        default=OutputTypeType.xcom
    )
    prompt: str = Field(
        description="An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language."
    )
    temperature: float = Field(
        description="What sampling temperature to use, between 0 and 2.",
        default=0.,
        gt=0.,
        le=2.
    )


class OutputModel(BaseModel):
    message: str = Field(
        description="Output message to log"
    )
    transcription_result: str = Field(
        default="",
        description="The result transcription text."
    )
    file_path: FilePath = Field(
        default="",
        description="The path to the results text file."
    )


class SecretsModel(BaseModel):
    OPENAI_API_KEY: str = Field(
        description="OpenAI API key"
    )