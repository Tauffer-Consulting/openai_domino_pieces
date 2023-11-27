from domino.testing import piece_dry_run, skip_envs
from pathlib import Path


test_file = str(Path(__file__).parent / "test-audio-to-transcribe.mp3")


@skip_envs('github')
def test_audio_transcription_piece():
    input_data = {
        "audio_file_path": test_file,
        "model_size": "tiny",
        "output_type": "both"
    }
    piece_output = piece_dry_run(
        piece_name="AudioTranscriptionLocalPiece",
        input_data=input_data,
    )
    assert piece_output["transcription_result"]
    assert piece_output["file_path_transcription_result"]
    assert "audio" in piece_output.get("transcription_result", "").lower()
