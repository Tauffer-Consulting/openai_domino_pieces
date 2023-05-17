from pydantic import BaseModel, Field, FilePath
from enum import Enum

class OutputTypeType(str, Enum):
    """
    Output type for the completion result
    """

    file = "file"
    string = "string"
    file_and_string = "file_and_string"


class LLMModelType(str, Enum):
    """
    The name of the model to use.
    Options: ada, babbage, curie, davinci
    """

    ada = "text-ada-001"
    babbage = "text-babbage-001"
    curie = "text-curie-001"
    davinci = "text-davinci-003"


class InputModel(BaseModel):
    """
    Completions Piece input model
    """

    prompt: str = Field(
        default=None,
        description="The prompt to use for the completion"
    )
    prompt_file_path: str = Field(
        default=None,
        description="Use only if not using prompt field. The path to a file containing the prompt to use for the completion. Must be .txt format",
    )
    output_type: OutputTypeType = Field(
        default=OutputTypeType.string,
        description="The type of output to return"
    )
    output_file_name: str = Field(
        default="completion_result.txt",
        description="It works only with Output Type = file. The name of the file to save the completion result"
    )
    llm_model_name: LLMModelType = Field(
        default=LLMModelType.babbage,
        description="The name of the model to use. Options: ada, babbage, curie, davinci"
    )
    max_tokens: int = Field(
        default=None,
        description="The maximum number of tokens to generate in the completion",
        gt=0
    )
    temperature: float = Field(
        default=1.,
        description="What sampling temperature to use, between 0 and 2",
        gt=0.,
        le=2.
    )


class OutputModel(BaseModel):
    """
    Completions Piece output model
    """
    
    message: str = Field(
        description="Output message to log"
    )
    string_completion_result: str = Field(
        default=None,
        description="The result of the completion as a string"
    )
    file_completion_result: FilePath = Field(
        default=None,
        description="The result of the completion as a .txt file"
    )
    usage_total_tokens: int = Field(
        description="The total number of tokens used in the completion"
    )


class SecretsModel(BaseModel):
    """
    Completions Piece secret model
    """

    OPENAI_API_KEY: str = Field(
        description="OpenAI API key"
    )