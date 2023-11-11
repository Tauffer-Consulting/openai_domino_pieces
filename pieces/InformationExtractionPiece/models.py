from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import List
from domino.models import OutputModifierModel, OutputModifierItemType


class LLMModelType(str, Enum):
    """
    OpenAI model type
    """
    gpt_3_5_turbo = "gpt-3.5-turbo-1106"
    gpt_4 = "gpt-4"


class InputModel(BaseModel):
    """
    InformationExtractionPiece Input model
    """
    input_text: str = Field(
        description='Source text from where information should be extracted.',
        json_schema_extra={"from_upstream": "always"}
    )
    openai_model: LLMModelType = Field(
        default=LLMModelType.gpt_3_5_turbo,
        description="OpenAI model name to use for information extraction.",
    )
    extract_items: List[OutputModifierModel] = Field(
        default=[
            OutputModifierModel(name="name", type=OutputModifierItemType.string, description="Name of the person."),
            OutputModifierModel(name="age", type=OutputModifierItemType.integer, description="Age of the person."),
        ],
        description='Information items to be extracted from source text.',
        json_schema_extra={"from_upstream": "never"}
    )


class OutputModel(BaseModel):
    """
    InformationExtractionPiece Output Model
    """
    # ref: https://docs.pydantic.dev/latest/concepts/models/#extra-fields
    model_config = ConfigDict(extra='allow')


class SecretsModel(BaseModel):
    """
    InformationExtractionPiece Secrets model
    """
    OPENAI_API_KEY: str = Field(description="Your OpenAI API key.")
