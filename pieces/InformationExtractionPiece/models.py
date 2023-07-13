from pydantic import BaseModel, Field, Extra
from domino.models import OutputModifierModel, OutputModifierItemType
from enum import Enum
from typing import List


class LLMModelType(str, Enum):
    """
    OpenAI model type
    """
    gpt_3_5_turbo = "gpt-3.5-turbo-0613"
    gpt_4 = "gpt-4"


class InputModel(BaseModel):
    """
    InformationExtractionPiece Input model
    """    
    input_text: str = Field(
        default=None,
        description='Source text from where information should be extracted.',
        from_upstream="always"
    )
    openai_model: LLMModelType = Field(
        default=LLMModelType.gpt_3_5_turbo,
        description="OpenAI model name to use for information extraction."
    )
    extract_items: List[OutputModifierModel] = Field(
        default=[
            OutputModifierModel(name="name", type=OutputModifierItemType.string, description="Name of the person"),
            OutputModifierModel(name="age", type=OutputModifierItemType.integer, description="Age of the person"),
        ],
        description='Information items to be extracted from source text.',
        from_upstream="never"
    )


class OutputModel(BaseModel, extra=Extra.allow):
    """
    InformationExtractionPiece Output Model
    """
    # ref: https://stackoverflow.com/a/75381426/11483674
    pass


class SecretsModel(BaseModel):
    """
    InformationExtractionPiece Secrets model
    """
    OPENAI_API_KEY: str = Field(
        description="Your OpenAI API key."
    )