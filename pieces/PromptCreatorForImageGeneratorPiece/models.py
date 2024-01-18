from pydantic import BaseModel, Field
from enum import Enum


class OutputTypeType(str, Enum):
    """
    Output type
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
    PromptCreatorForImageGeneratorPiece input model
    """
    context: str = Field(
        ...,
        description="The context to generate an image from",
    )
    art_style: str = Field(
        default="You know many art styles, so you always vary a lot on your suggestions!",
        description="The art style to generate an image from. Your imagination is the limit!"
    )
    output_type: OutputTypeType = Field(
        default=OutputTypeType.string,
        description="The type of output to return"

    )
    openai_model: LLMModelType = Field(
        default=LLMModelType.gpt_3_5_turbo,
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
    PromptCreatorForImageGeneratorPiece output model
    """
    generated_prompt_string: str = Field(
        default=None,
        description="The generated prompt to pass to an image generator AI",
    )
    generated_prompt_file_path: str = Field(
        default=None,
        description="The path to the generated prompt, in .txt format",
    )


class SecretsModel(BaseModel):
    """
    PromptCreatorForImageGeneratorPiece secrets model
    """
    OPENAI_API_KEY: str = Field(
        description="Your OpenAI API key"
    )