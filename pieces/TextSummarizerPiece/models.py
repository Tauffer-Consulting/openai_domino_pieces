from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class OutputTypeType(str, Enum):
    """
    Output type for the completion result
    """
    file = "file"
    string = "string"
    file_and_string = "file_and_string"


class LLMModelType(str, Enum):
    """
    OpenAI model type
    """
    gpt_3_5_turbo = "gpt-3.5-turbo"
    gpt_4 = "gpt-4"


class InputModel(BaseModel):
    """
    TextSummarizerPiece Input model
    """
    text: Optional[str] = Field(
        default=None,
        description="Text to summarize",
        json_schema_extra={
            'widget': "textarea",
        }
    )
    text_file_path: Optional[str] = Field(
        default=None,
        description="Use it only if not using text field. File path to the text to summarize",
        json_schema_extra={
            "from_upstream": "always"
        }
    )
    output_type: OutputTypeType = Field(
        default=OutputTypeType.string,
        description="The type of output to return"
    )
    openai_model: LLMModelType = Field(
        default=LLMModelType.gpt_3_5_turbo,
        description="OpenAI model name to use for summarization"
    )
    chunk_size: int = Field(
        default=1000,
        description="Chunk size, measured in tokens, of each pre-summary chunk"
    )
    chunk_overlap_rate: float = Field(
        default=0.2,
        description="The percentage of overlap between each chunk"
    )
    completion_max_tokens: int = Field(
        default=500,
        description="The maximum number of tokens to generate in the summary."
    )
    temperature: float = Field(
        description="Temperature of the model, between 0 (more precise) and 1 (more creative)",
        default=0.2
    )


class OutputModel(BaseModel):
    """
    TextSummarizerPiece Output model
    """
    string_summarized_text: str = Field(
        default=None,
        description="summarized text"
    )
    file_path_summarized_text: str = Field(
        default=None,
        description="Path to summarized text file"
    )


class SecretsModel(BaseModel):
    """
    TextSummarizerPiece Secrets model
    """
    OPENAI_API_KEY: str = Field(
        description="Your OpenAI API key"
    )