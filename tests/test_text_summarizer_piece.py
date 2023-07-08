from domino.scripts.piece_dry_run import piece_dry_run
from dotenv import load_dotenv
from pathlib import PosixPath
from pydantic import FilePath
import tiktoken
import os

def run_piece(
        output_type: str,
        completion_max_tokens: int,
        text: str = None,
        text_file_path: FilePath = None,
        chunk_size: int = 1000,
        chunk_overlap_rate: float = 0.2,
        openai_model: str = "gpt-3.5-turbo",
        temperature: float = 0.1,
):
    
    load_dotenv()
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    return piece_dry_run(
    
    #local piece repository path
    repository_folder_path="../",

    #name of the piece
    piece_name="TextSummarizerPiece",

    #values to the InputModel arguments
    piece_input={
        "output_type": output_type,
        "completion_max_tokens": completion_max_tokens,
        "text": text,
        "text_file_path": text_file_path,
        "chunk_size": chunk_size,
        "chunk_overlap_rate": chunk_overlap_rate,
        "openai_model": openai_model,
        "temperature": temperature,
    },    
    #values to the SecretModel arguments
    secrets_input={ 
        "OPENAI_API_KEY": OPENAI_API_KEY
    }
)

def test_piece():
    text = """
In the realm of surrealistic oceanic exploration, a team of intrepid divers embarks on a mesmerizing journey into an underwater city. With every dive, they plunge into a world of wonder and discovery, where the laws of nature blend with the imaginative depths of the human mind. The vast expanse of the underwater city unfolds before their eyes, adorned with ethereal bioluminescent hues and architectural wonders that defy imagination.
As the divers navigate through the otherworldly landscapes, they are drawn deeper into the enigma of the submerged city. Mysterious symbols, etched into ancient walls and forgotten structures, beckon them to unlock the secrets hidden within. Each stroke of their brushes, capturing the essence of the symbols, reveals fragments of a forgotten past. The artistry of their exploration intertwines with the artistry of the city, creating a harmonious dance of curiosity and revelation.
Within the surrealistic tapestry of this underwater world, the divers unearth evidence of an advanced civilization. Marvels of technology, meticulously preserved, whisper stories of innovation and progress that surpass their wildest dreams. Every artifact becomes a brushstroke in a larger narrative, painting a picture of a lost culture's brilliance. With each stroke of their brushes, the divers bring the past to life, ensuring that the legacy of this extraordinary underwater city will endure in the annals of human history."""

    piece_kwargs = {
        "text": text,
        "output_type": "file_and_string",
        "completion_max_tokens": 500,
        "openai_model": "gpt-3.5-turbo",
    }

    output = run_piece(
        **piece_kwargs
    )

    if piece_kwargs["output_type"] == "file":
        assert output.string_summarized_text == None
        assert type(output.file_path_summarized_text) == PosixPath and output.file_path_summarized_text.name.endswith(".txt")
        generated_prompt = output.file_path_summarized_text.read_text()
    if piece_kwargs["output_type"] == "string":
        assert output.string_summarized_text != None and type(output.string_summarized_text) == str
        assert output.file_path_summarized_text == None
        generated_prompt = output.string_summarized_text
    if piece_kwargs["output_type"] == "file_and_string":
        assert output.string_summarized_text != None and type(output.string_summarized_text) == str
        assert type(output.file_path_summarized_text) == PosixPath and output.file_path_summarized_text.name.endswith(".txt")
        generated_prompt = output.string_summarized_text
    
    encoding = tiktoken.encoding_for_model(piece_kwargs["openai_model"])
    text_tokens = encoding.encode(text=generated_prompt)
    assert len(text_tokens) <= piece_kwargs["completion_max_tokens"]

    
    


if __name__ == "__main__":
    test_piece()
