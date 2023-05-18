from pydantic import BaseModel, Field, FilePath
from enum import Enum


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


class InputModel(BaseModel):
    """
    StorytellerCharacterPiece input model
    """
    character_name: str = Field(
        ...,
        description="Your character's name",
    )
    character_description: str = Field(
        ...,
        description="Your character's description",
    )
    previous_stories_file_path: FilePath = Field(
        default=None,
        description="Path to your character's previous stories. Must be a .txt file",
    )
    openai_model: LLMModelType = Field(
        default=LLMModelType.gpt_3_5_turbo,
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
    """
    StorytellerCharacterPiece output model
    """
    new_story: str = Field(
        description="Your new story",
    )
    new_story_with_character_info: str = Field(
        description="Your new story with your character's name and description"
    )
    stories_file_path: FilePath = Field(
        description="Path to your stories including the new one."
    )


class SecretsModel(BaseModel):
    """
    StorytellerCharacterPiece secrets model
    """    
    OPENAI_API_KEY: str = Field(
        description="Your OpenAI API key"
    )