from pydantic import BaseModel, Field
from enum import Enum

class LLMModelType(str, Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"

class InputModel(BaseModel):
    """MyNewPiece Input"""
    context: str = Field(
        default=None,
        description="The context to generate an image from",
    )

    openai_model: LLMModelType = Field(
        default=LLMModelType.GPT_3_5_TURBO,
        description="OpenAI model to bring your character to life"
    )

    completion_max_tokens: int = Field(
        default=500,
        description="The maximum number of tokens to generate the new history."
    )

    temperature: float = Field(
        default=0.7,
        description="Temperature of the model, between 0 (more precise) and 1 (more creative)"
    )

class OutputModel(BaseModel):
    """MyNewPiece Output"""
    generated_prompt: str = Field(
        description="The generated prompt to pass to an image generator AI",
    )

    prompt_file_path: str = Field(
        description="The path to the generated prompt, in .txt format",
    )

class SecretsModel(BaseModel):
    """MyNewPiece Secrets"""
    
    OPENAI_API_KEY: str = Field(
        description="Your OpenAI API key"
    )