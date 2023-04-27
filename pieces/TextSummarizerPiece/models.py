from pydantic import BaseModel, Field
from enum import Enum
class LLMModelType(str, Enum):
    gpt_3_5_turbo = "gpt-3.5-turbo"
    gpt_4 = "gpt-4"
class InputModel(BaseModel):
    """Text Summarizer Piece"""    
    text: str = Field(
        default="",
        description="Text to summarize",
    )

    chunk_size: int = Field(
        default=1000,
        description="Chunk size of each pre-summary chunk"
    )

    chunk_overlap: int = Field(
        default=20,
        description="Chunk overlap of each pre-summary chunk"
    )

    openai_model_name: LLMModelType = Field(
        default=LLMModelType.gpt_3_5_turbo,
        description="OpenAI model name to use for summarization"
    )

    max_tokens: int = Field(
        default=None,
        description="The maximum number of tokens to generate in the summary."
    )

    temperature: float = Field(
        description="Temperature of the model, between 0 (more precise) and 1 (more creative)",
        default=0.2
    )


class OutputModel(BaseModel):
    """Text Summarizer Piece"""

    summarized_text: str = Field(
        description="summarized text"
    )

class SecretsModel(BaseModel):
    """
    Text Summarizer Piece Secrets
    """

    OPENAI_API_KEY: str = Field(
        description="Your OpenAI API key"
    )