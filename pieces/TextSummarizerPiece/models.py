from pydantic import BaseModel, Field
from enum import Enum
class LLMModelType(str, Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"

class InputModel(BaseModel):
    """
    Text Summarizer Piece
    """    

    text: str = Field(
        default=None,
        description="Text to summarize",
    )
    text_file_path: str = Field(
        default=None,
        description="Use it only if not using text field. File path to the text to summarize"
    )
    output_file_name: str = Field(
        default="summarized_text.txt",
        description="Name of output file"
    )
    openai_model: LLMModelType = Field(
        default=LLMModelType.GPT_3_5_TURBO,
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
    Text Summarizer Piece Output
    """

    summarized_text: str = Field(
        description="summarized text"
    )

    summarized_text_file_path: str = Field(
        description="Path to summarized text file"
    )

class SecretsModel(BaseModel):
    """
    Text Summarizer Piece Secrets
    """

    OPENAI_API_KEY: str = Field(
        description="Your OpenAI API key"
    )