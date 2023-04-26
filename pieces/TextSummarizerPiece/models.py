from pydantic import BaseModel, Field

class InputModel(BaseModel):
    """Text Summarizer Piece"""

    prompt_template: str = Field(
        default="""Write a summary of the given text while maintaining its original writing form.

text:
    
{text}

CONCISE SUMMARY:""",
        description="Prompt template to use for summarization"
    )
    
    text: str = Field(
        default="",
        description="Text to summarize",
    )

    openai_model_name: str = Field(
        default="gpt-3.5-turbo",
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