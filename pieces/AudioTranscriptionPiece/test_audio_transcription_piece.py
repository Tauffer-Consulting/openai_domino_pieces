import pytest
from domino.testing import piece_dry_run
import os


def run_piece(
    audio_file_path: str,
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


@pytest.mark.skip(reason="Skipping until we have a test audio file")
def test_piece():
    piece_kwargs = {
        "audio_file_path": "",
        "output_type": "file_and_string",
    }

    output = run_piece(
        **piece_kwargs
    )

    if piece_kwargs["output_type"] == "file":
        assert output.get("string_transcription_result") == None
        assert output.get("file_path_transcription_result").endswith(".txt")
    if piece_kwargs["output_type"] == "string":
        assert output.get("string_transcription_result") != None and type(output.get("string_transcription_result")) == str
        assert output.get("file_path_transcription_result") == None
    if piece_kwargs["output_type"] == "file_and_string":
        assert output.get("string_transcription_result") != None and type(output.get("string_transcription_result")) == str
        assert output.get("file_path_transcription_result").endswith(".txt")