from pydantic import BaseModel, Field
from enum import Enum
class LLMModelType(tuple, Enum):
    GPT_3_5_TURBO = ("gpt-3.5-turbo", 4000)
    GPT_4 = ("gpt-4", 8000)

    @property
    def model_name(self):
        return self.value[0]

    @property
    def token_limits(self):
        return self.value[1]

class InputModel(BaseModel):
    """Text Summarizer Piece"""    
    text: str = Field(
        default="",
        description="Text to summarize",
    )

    chunk_size: int = Field(
        default=1000,
        description="Chunk size, measured in tokens, of each pre-summary chunk"
    )

    chunk_overlap_rate: float = Field(
        default=0.2,
        description="The percentage of overlap between each chunk"
    )

    openai_model: LLMModelType = Field(
        default=LLMModelType.GPT_3_5_TURBO,
        description="OpenAI model name to use for summarization"
    )

    max_tokens: int = Field(
        default=500,
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