from pydantic import BaseModel, Field, FilePath
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
    art_style: str = Field(
        default="You know many art styles, so you always vary a lot on your suggestions!",
        description="The art style to generate an image from. Your imagination is the limit!",
    )
    output_type: OutputTypeType = Field(
        default=OutputTypeType.string,
        description="The type of output to return"
    )
    output_file_name: str = Field(
        default="generated_prompt.txt",
        description="It works only with Output Type = file. The name of the file to save the generated prompt"
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
    generated_prompt_file_path: FilePath = Field(
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