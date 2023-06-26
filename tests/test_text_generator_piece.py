from domino.scripts.piece_dry_run import piece_dry_run
from dotenv import load_dotenv
from pathlib import PosixPath
from pydantic import FilePath
from typing import List
import tiktoken
import os

def run_piece(
       template: str,
       prompt_args: List[dict],
       output_type: str,
       openai_model: str,
       completion_max_tokens: int,
       temperature: float = 0.3
):
    
    load_dotenv()
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    return piece_dry_run(
    
    #local piece repository path
    repository_folder_path="../",

    #name of the piece
    piece_name="TextGeneratorPiece",

    #values to the InputModel arguments
    piece_input={
        "template": template,
        "prompt_args": prompt_args,
        "output_type": output_type,
        "completion_max_tokens": completion_max_tokens,
        "openai_model": openai_model,
        "temperature": temperature,
    },    
    #values to the SecretModel arguments
    secrets_input={ 
        "OPENAI_API_KEY": OPENAI_API_KEY
    }
)

def test_piece():
    template = "tell me about the history of {event_history}"
    prompt_args = [{"arg_name": "event_history", "arg_value": "artifical intelligence"}]

    piece_kwargs = {
        "template": template,
        "prompt_args": prompt_args,
        "output_type": "file",
        "completion_max_tokens": 500,
        "openai_model": "gpt-3.5-turbo",
    }

    output = run_piece(
        **piece_kwargs
    )

    if piece_kwargs["output_type"] == "file":
        assert output.string_generated_text == None
        assert type(output.file_path_generated_text) == PosixPath and output.file_path_generated_text.name.endswith(".txt")
        generated_prompt = output.file_path_generated_text.read_text()
    if piece_kwargs["output_type"] == "string":
        assert output.string_generated_text != None and type(output.string_generated_text) == str
        assert output.file_path_generated_text == None
        generated_prompt = output.string_generated_text
    if piece_kwargs["output_type"] == "file_and_string":
        assert output.string_generated_text != None and type(output.string_generated_text) == str
        assert type(output.file_path_generated_text) == PosixPath and output.file_path_generated_text.name.endswith(".txt")
        generated_prompt = output.string_generated_text
    
    encoding = tiktoken.encoding_for_model(piece_kwargs["openai_model"])
    text_tokens = encoding.encode(text=generated_prompt)
    assert len(text_tokens) <= piece_kwargs["completion_max_tokens"]


if __name__ == "__main__":
    test_piece()
