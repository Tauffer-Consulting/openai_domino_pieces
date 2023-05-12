from pydantic import BaseModel, Field
from enum import Enum

class LLMModelType(str, Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"

class InputModel(BaseModel):
    """MyNewPiece Input"""
    character_name: str = Field(
        ...,
        description="Your character's name",
    )

    character_description: str = Field(
        ...,
        description="Your character's description",
    )

    previous_stories_file_path: str = Field(
        default=None,
        description="Path to your character's previous stories. Must be a .txt file",
    )

    openai_model: LLMModelType = Field(
        default=LLMModelType.GPT_3_5_TURBO,
        description="OpenAI model to bring your character to life"
    )

    completion_max_tokens: int = Field(
        default=500,
        description="The maximum number of tokens to generate the new history."
    )

    temperature: float = Field(
        default=0.5,
        description="Temperature of the model, between 0 (more precise) and 1 (more creative)",
        gt=0,
        lt=1
    )


class OutputModel(BaseModel):
    """MyNewPiece Output"""

    new_story: str = Field(
        description="Your new story",
    )

    new_story_with_character_info: str = Field(
        description="Your new story with your character's name and description"
    )
    
    stories_file_path: str = Field(
        description="Path to your stories including the new one."
    )

class SecretsModel(BaseModel):
    """MyNewPiece Secrets"""
    
    OPENAI_API_KEY: str = Field(
        description="Your OpenAI API key"
    )