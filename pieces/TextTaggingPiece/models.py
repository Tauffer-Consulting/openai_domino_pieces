from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import List
from domino.models import (
    OutputModifierModel as OutputModifierModelBase,
    OutputModifierItemType
)


class LLMModelType(str, Enum):
    """
    OpenAI model type
    """
    gpt_3_5_turbo = "gpt-3.5-turbo-1106"
    gpt_4 = "gpt-4"


class OutputModifierModel(OutputModifierModelBase):
    """
    OutputModifierModel with extra fields
    """
    enum: str = Field(
        default="",
        description="Comma separated list of possible values for the output modifier. Example: 'negative,neutral,positive'. If not provided, this will be ignored. ",
    )


class InputModel(BaseModel):
    """
    TextTaggingPiece Input model
    """
    input_text: str = Field(
        description='Source text to be tagged.',
    )
    openai_model: LLMModelType = Field(
        default=LLMModelType.gpt_3_5_turbo,
        description="OpenAI model name to use for tagging.",
    )
    tags: List[OutputModifierModel] = Field(
        default=[
            OutputModifierModel(name="sentiment", type=OutputModifierItemType.float, description="Sentiment of the text. Should be a number between -1 and 1."),
        ],
        description='Tags to classify the source text.',
        json_schema_extra={"from_upstream": "never"}
    )
    temperature: float = Field(
        default=0.,
        description="Temperature of the model, between 0 (more precise) and 1 (more creative).",
        gt=0.,
        lt=1.
    )


class OutputModel(BaseModel):
    """
    TextTaggingPiece Output Model
    """
    # ref: https://docs.pydantic.dev/latest/concepts/models/#extra-fields
    model_config = ConfigDict(extra='allow')


class SecretsModel(BaseModel):
    """
    TextTaggingPiece Secrets model
    """
    OPENAI_API_KEY: str = Field(description="Your OpenAI API key.")
