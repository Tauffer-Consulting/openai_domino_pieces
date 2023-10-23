from domino.testing import piece_dry_run
from pathlib import PosixPath
from pydantic import FilePath
import os


def run_piece(
    audio_file_path: FilePath,
    output_type: str,
    temperature: float = 0.1,
):
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    return piece_dry_run(
        piece_name="AudioTranscriptionPiece",
        input_data={
            "audio_file_path": audio_file_path,
            "output_type": output_type,
            "temperature": temperature
        },
        secrets_data={ 
            "OPENAI_API_KEY": OPENAI_API_KEY
        }
)

def test_piece():
    piece_kwargs = {
        "audio_file_path": "",
        "output_type": "file_and_string",
    }

    output = run_piece(
        **piece_kwargs
    )

    if piece_kwargs["output_type"] == "file":
        assert output.string_transcription_result == None
        assert type(output.file_path_transcription_result) == PosixPath and output.file_path_transcription_result.name.endswith(".txt")
    if piece_kwargs["output_type"] == "string":
        assert output.string_transcription_result != None and type(output.string_transcription_result) == str
        assert output.file_path_transcription_result == None
    if piece_kwargs["output_type"] == "file_and_string":
        assert output.string_transcription_result != None and type(output.string_transcription_result) == str
        assert type(output.file_path_transcription_result) == PosixPath and output.file_path_transcription_result.name.endswith(".txt")