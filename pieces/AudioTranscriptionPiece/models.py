from pydantic import BaseModel, Field
from enum import Enum


class OutputTypeType(str, Enum):
    file = "file"
    string = "string"
    both = "both"


class InputModel(BaseModel):
    audio_file_path: str = Field(
        description='The path to the audio file to process.',
        json_schema_extra={
            "from_upstream": "always"
        }
    )
    output_type: OutputTypeType = Field(
        default=OutputTypeType.string,
        description='The type of output for the result text. Options are `string`, `file` or `both`. Default is `string`.',
    )
    temperature: float = Field(
        description="What sampling temperature to use, between 0 and 1",
        default=0.1,
        gt=0.,
        le=1,

    )


class OutputModel(BaseModel):
    transcription_result: str = Field(
        default="",
        description="The result transcription text as a string."
    )
    file_path_transcription_result: str = Field(
        default="",
        description="The path to the text file with the transcription result."
    )


class SecretsModel(BaseModel):
    OPENAI_API_KEY: str = Field(
        description="OpenAI API key"
    )
