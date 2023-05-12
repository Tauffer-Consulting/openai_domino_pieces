from pydantic import BaseModel, Field
from enum import Enum

class LLMModelType(str, Enum):
    """
    OpenAI model types
    """

    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"

class InputModel(BaseModel):
    """
    Prompt For Image Generator Piece Input
    """

    context: str = Field(
        ...,
        description="The context to generate an image from",
    )
    output_file_name: str = Field(
        default=None,
        description="Use it only if you want to save the prompt result to a file in addition to the string output"
    )
    openai_model: LLMModelType = Field(
        default=LLMModelType.GPT_3_5_TURBO,
        description="OpenAI model to bring your character to life"
    )
    completion_max_tokens: int = Field(
        default=350,
        description="The maximum number of tokens to generate the prompt."
    )
    temperature: float = Field(
        default=0.7,
        description="Temperature of the model, between 0 (more precise) and 1 (more creative)",
        gt=0,
        le=1
    )

class OutputModel(BaseModel):
    """
    Prompt For Image Generator Piece Output
    """

    generated_prompt_string: str = Field(
        description="The generated prompt to pass to an image generator AI",
    )
    generated_prompt_file_path: str = Field(
        default=None,
        description="The path to the generated prompt, in .txt format",
    )

class SecretsModel(BaseModel):
    """
    Prompt For Image Generator Piece Secrets
    """    

    OPENAI_API_KEY: str = Field(
        description="Your OpenAI API key"
    )