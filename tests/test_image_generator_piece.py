from domino.scripts.piece_dry_run import piece_dry_run
from dotenv import load_dotenv
from pathlib import PosixPath
import os

def run_piece(
        prompt: str,
        image_format: str,
        output_type: str,
        size: str = "1024x1024",
):
    
    load_dotenv()
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    return piece_dry_run(
    
    #local piece repository path
    repository_folder_path="../",

    #name of the piece
    piece_name="ImageGeneratorPiece",

    #values to the InputModel arguments
    piece_input={
        "prompt": prompt,
        "image_format": image_format,
        "output_type": output_type,
        "size": size
    },    
    #values to the SecretModel arguments
    secrets_input={ 
        "OPENAI_API_KEY": OPENAI_API_KEY
    }
)

def test_piece():
    piece_kwargs = {
        "prompt": "draw a punk art style painting",
        "image_format": "base64_string",
        "output_type": "file_and_string",
        "size": "512x512",
    }

    output = run_piece(
        **piece_kwargs
    )

    if piece_kwargs["image_format"] == "url":
        if piece_kwargs["output_type"] == "file":
            assert output.output_string == None
            assert type(output.output_file_path) == PosixPath and output.output_file_path.name.endswith(".txt")
        if piece_kwargs["output_type"] == "string":
            assert output.output_string != None and type(output.output_string) == str
            assert output.output_file_path == None
        if piece_kwargs["output_type"] == "file_and_string":
            assert output.output_string != None and type(output.output_string) == str
            assert type(output.output_file_path) == PosixPath and output.output_file_path.name.endswith(".txt")
    if piece_kwargs["image_format"] == "image_png":
        if piece_kwargs["output_type"] == "file":
            assert output.output_string == None
            assert type(output.output_file_path) == PosixPath and output.output_file_path.name.endswith(".png")
        if piece_kwargs["output_type"] == "string":
            assert output.output_string == None
            assert type(output.output_file_path) == PosixPath and output.output_file_path.name.endswith(".png")
        if piece_kwargs["output_type"] == "file_and_string":
            assert output.output_string == None
            assert type(output.output_file_path) == PosixPath and output.output_file_path.name.endswith(".png")
    if piece_kwargs["image_format"] == "base64_string":
        if piece_kwargs["output_type"] == "file":
            assert output.output_string == None
            assert type(output.output_file_path) == PosixPath and output.output_file_path.name.endswith(".txt")
        if piece_kwargs["output_type"] == "string":
            assert output.output_string != None and type(output.output_string) == str
            assert output.output_file_path == None
        if piece_kwargs["output_type"] == "file_and_string":
            assert output.output_string != None and type(output.output_string) == str
            assert type(output.output_file_path) == PosixPath and output.output_file_path.name.endswith(".txt")

if __name__ == "__main__":
    test_piece()
