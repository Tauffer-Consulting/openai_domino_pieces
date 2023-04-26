from pydantic import BaseModel, Field

class InputModel(BaseModel):
    """Text Summarizer Piece"""

    text: str = Field(
        default="",
        description="text to summarize",
    )

    openai_model_name: str = Field(
        default="gpt-3.5-turbo",
        description="model name to use for summarization"
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