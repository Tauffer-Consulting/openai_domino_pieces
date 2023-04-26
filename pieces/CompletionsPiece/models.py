from pydantic import BaseModel, Field
from enum import Enum


class LLMModelType(str, Enum):
    ada = "text-ada-001"
    babbage = "text-babbage-001"
    curie = "text-curie-001"
    davinci = "text-davinci-003"


class InputModel(BaseModel):
    llm_model_name: LLMModelType = Field(
        description="The name of the model to use. Options: ada, babbage, curie, davinci"
    )
    prompt: str = Field(
        description="The prompt to use for the completion"
    )
    max_tokens: int = Field(
        description="The maximum number of tokens to generate in the completion.",
        default=16,
        gt=0
    )
    temperature: float = Field(
        description="What sampling temperature to use, between 0 and 2.",
        default=1.,
        gt=0.,
        le=2.
    )


class OutputModel(BaseModel):
    message: str = Field(
        description="Output message to log"
    )
    result_text: str = Field(
        description="The result of the text completion."
    )
    usage_total_tokens: int = Field(
        description="The total number of tokens used in the completion."
    )


class SecretsModel(BaseModel):
    OPENAI_API_KEY: str = Field(
        description="OpenAI API key"
    )