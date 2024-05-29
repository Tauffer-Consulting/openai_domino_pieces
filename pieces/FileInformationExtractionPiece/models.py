from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import List
from domino.models import OutputModifierModel, OutputModifierItemType
from typing import Optional

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
    input_file_path: str = Field(
        description='Source text from where information should be extracted.',
        json_schema_extra={"from_upstream": "always"}
    )
    additional_information: Optional[str] = Field(
        default=None,
        description='Additional useful information to help with the extraction.',
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
    output_data: List[dict] = Field(description="Extracted information as JSON.")
    # output_file_path: str = Field(description="Extracted information as json file.")

class SecretsModel(BaseModel):
    """
    InformationExtractionPiece Secrets model
    """
    OPENAI_API_KEY: str = Field(description="Your OpenAI API key.")
