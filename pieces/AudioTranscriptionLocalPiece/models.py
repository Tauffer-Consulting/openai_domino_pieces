from pydantic import BaseModel, Field, FilePath
from typing import Union
from enum import Enum


class ModelSizeType(str, Enum):
    tiny = "tiny"
    base = "base"
    small = "small"
    medium = "medium"
    large = "large"


class OutputTypeType(str, Enum):
    string = "string"
    file = "file"
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
    model_size: ModelSizeType = Field(
        description='The size of the model to use. Default is tiny.',
        default=ModelSizeType.tiny
    )


class OutputModel(BaseModel):
    transcription_result: str = Field(
        default="",
        description="The result transcription text as a string."
    )
    file_path_transcription_result: Union[FilePath, str] = Field(
        default="",
        description="The path to the text file with the transcription result."
    )
