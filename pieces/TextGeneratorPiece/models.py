from pydantic import BaseModel, Field
from enum import Enum
from typing import List

class LLMModelType(str, Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"

class InnerArgModel(BaseModel):
    arg_name: str
    arg_value: str

class InputModel(BaseModel):
    """
    Text Generator Input
    """

    template: str = Field(
        ...,
        description="Compose a prompt template using the { } notation to insert arguments into the prompt itself",
    )
    prompt_args: List[InnerArgModel] = Field(
        default=None,
        description="List of arguments to insert into the prompt.",

    )
    # prompt_params: dict = Field(
    #     ...,
    #     description="Parameters to insert into the prompt. Write as a python dictionary with the paramter name as the key and the parameter value as the value",
    # )
    openai_model: LLMModelType = Field(
        default=LLMModelType.GPT_3_5_TURBO,
        description="OpenAI model to bring your character to life"
    )
    completion_max_tokens: int = Field(
        default=500,
        description="The maximum number of tokens to generate the text."
    )
    temperature: float = Field(
        default=0.3,
        description="Temperature of the model, between 0 (more precise) and 1 (more creative)",
        gt=0,
        lt=1
    )


class OutputModel(BaseModel):
    """
    Text Generator Output
    """

    generated_text: str = Field(
        description="The generated text",
    )

class SecretsModel(BaseModel):
    """
    Text Generator Secrets
    """
    
    OPENAI_API_KEY: str = Field(
        description="Your OpenAI API key"
    )