from pydantic import BaseModel, Field, FilePath
from enum import Enum
from typing import List, Union


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
    ada = "text-ada-001"
    babbage = "text-babbage-001"
    curie = "text-curie-001"
    davinci = "text-davinci-003"


class ArgType(str, Enum):
    string = "string"
    integer = "integer"
    float = "float"
    boolean = "boolean"


class InnerArgModel(BaseModel):
    """
    Inner argument model to use in the prompt args
    """

    arg_name: str
    arg_value: str
    arg_type: ArgType


class InputModel(BaseModel):
    """
    TextGeneratorPiece Input model
    """

    template: str = Field(
        default="What is the capital city of {country}?",
        description="Compose a prompt template using the { } notation to insert arguments.",
    )
    prompt_args: List[InnerArgModel] = Field(
        default=None,
        description="List of arguments to insert into the prompt.",
    )
    output_type: OutputTypeType = Field(
        default=OutputTypeType.string, description="The type of output to return."
    )
    output_file_name: str = Field(
        default="generated_text.txt",
        description="It works only with Output Type = file. The name of the file to save the generated text.",
    )
    openai_model: LLMModelType = Field(
        default=LLMModelType.gpt_3_5_turbo, description="OpenAI model name."
    )
    completion_max_tokens: int = Field(
        default=500, description="The maximum number of tokens in the generated text."
    )
    temperature: float = Field(
        default=0.3,
        description="Temperature of the model, between 0 (more precise) and 1 (more creative).",
        gt=0,
        lt=1,
    )


class OutputModel(BaseModel):
    """
    TextGeneratorPiece Output model
    """

    string_generated_text: str = Field(
        default=None, description="The generated text as a string"
    )
    file_path_generated_text: FilePath = Field(
        default=None, description="The path to text file containing generated text"
    )


class SecretsModel(BaseModel):
    """
    TextGeneratorPiece Secrets model
    """

    OPENAI_API_KEY: str = Field(description="Your OpenAI API key")


if __name__ == "__main__":
    input_model_schema = InputModel.schema_json()
    print(input_model_schema)
