from domino.scripts.piece_dry_run import piece_dry_run
from dotenv import load_dotenv
from pathlib import PosixPath
import tiktoken
import os

def run_piece(
        context: str,
        art_style: str,
        output_type: str,
        completion_max_tokens: int,
        openai_model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
):
    
    load_dotenv()
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    return piece_dry_run(
    
    #local piece repository path
    repository_folder_path="../",

    #name of the piece
    piece_name="PromptCreatorForImageGeneratorPiece",

    #values to the InputModel arguments
    piece_input={
        "context": context,
        "art_style": art_style,
        "completion_max_tokens": completion_max_tokens,
        "output_type": output_type,
        "openai_model": openai_model,
        "temperature": temperature
    },    
    #values to the SecretModel arguments
    secrets_input={ 
        "OPENAI_API_KEY": OPENAI_API_KEY
    }
)

def test_piece():
    piece_kwargs = {
        "context": "Explorers dive into a mesmerizing underwater city, discovering ancient secrets, mysterious symbols, and evidence of an advanced civilization.",
        "art_style": "surrealistic oceanic exploration",
        "completion_max_tokens": 350,
        "output_type": "file",
        "openai_model": "gpt-3.5-turbo",
        "temperature": 0.7,
    }

    output = run_piece(
        **piece_kwargs
    )

    if piece_kwargs["output_type"] == "file":
        assert output.generated_prompt_string == None
        assert type(output.generated_prompt_file_path) == PosixPath and output.generated_prompt_file_path.name.endswith(".txt")
        generated_prompt = output.generated_prompt_file_path.read_text()
    if piece_kwargs["output_type"] == "string":
        assert output.generated_prompt_string != None and type(output.generated_prompt_string) == str
        assert output.generated_prompt_file_path == None
        generated_prompt = output.generated_prompt_string
    if piece_kwargs["output_type"] == "file_and_string":
        assert output.generated_prompt_string != None and type(output.generated_prompt_string) == str
        assert type(output.generated_prompt_file_path) == PosixPath and output.generated_prompt_file_path.name.endswith(".txt")
        generated_prompt = output.generated_prompt_string
    
    encoding = tiktoken.encoding_for_model(piece_kwargs["openai_model"])
    text_tokens = encoding.encode(text=generated_prompt)
    assert len(text_tokens) <= piece_kwargs["completion_max_tokens"]

    
    


if __name__ == "__main__":
    test_piece()
