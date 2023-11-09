from pydantic import BaseModel, Field
from enum import Enum
from typing import List


class OutputTypeType(str, Enum):
    """
    Output type for the generated text
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


class InnerArgModel(BaseModel):
    """
    Inner argument model to use in the prompt args
    """
    arg_name: str = Field(
        description='Name of the prompt argument.',
        json_schema_extra={
            "from_upstream": "never"
        }
    )
    arg_value: str = Field(
        description='Value of the prompt argument.',
        
    )


class InputModel(BaseModel):
    """
    TextGeneratorPiece Input model
    """
    template: str = Field(
        default="What is the capital city of {country}?",
        description="Compose a prompt template using the {arg_name} notation to insert arguments."
    )
    prompt_args: List[InnerArgModel] = Field(
        default=[InnerArgModel(arg_name="country", arg_value="Brazil")],
        description="List of arguments to insert into the prompt."
    )
    output_type: OutputTypeType = Field(
        default=OutputTypeType.string, 
        description="The type of output to return."
    )
    openai_model: LLMModelType = Field(
        default=LLMModelType.gpt_3_5_turbo, 
        description="OpenAI model name."
    )
    completion_max_tokens: int = Field(
        default=500, 
        description="The maximum number of tokens in the generated text."
    )
    temperature: float = Field(
        default=0.3,
        description="Temperature of the model, between 0 (more precise) and 1 (more creative).",
        gt=0,
        lt=1
    )


class OutputModel(BaseModel):
    """
    TextGeneratorPiece Output model
    """
    string_generated_text: str = Field(
        default=None, 
        description="The generated text as a string"
    )
    file_path_generated_text: str = Field(
        default=None, 
        description="The path to text file containing generated text"
    )


class SecretsModel(BaseModel):
    """
    TextGeneratorPiece Secrets model
    """
    OPENAI_API_KEY: str = Field(description="Your OpenAI API key")

