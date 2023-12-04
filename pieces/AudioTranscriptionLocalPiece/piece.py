from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import whisper
from pathlib import Path


class AudioTranscriptionLocalPiece(BasePiece):

    def piece_function(self, input_data: InputModel):

        self.logger.info("Loading model...")
        model = whisper.load_model(input_data.model_size)

        self.logger.info("Transcribing audio file...")
        result = model.transcribe(str(input_data.audio_file_path))["text"]

        if input_data.output_type == "string":
            self.logger.info("Transcription complete successfully. Result returned as string.")
            transcription_result = result
            output_file_path = ""
        elif input_data.output_type == "file":
            self.logger.info("Transcription complete successfully. Result returned as file.")
            transcription_result = ""
            output_file_path = str(Path(self.results_path) / "transcription_result.txt")
            with open(output_file_path, "w") as f:
                f.write(result)
        else:
            self.logger.info("Transcription complete successfully. Result returned as string and file.")
            transcription_result = result
            output_file_path = str(Path(self.results_path) / "transcription_result.txt")
            with open(output_file_path, "w") as f:
                f.write(result)

        print("LOGGER", output_file_path)
        # Display result in the Domino GUI
        self.format_display_result(input_data=input_data, string_transcription_result=result)

        return OutputModel(
            transcription_result=transcription_result,
            file_path_transcription_result=output_file_path
        )

    def format_display_result(self, input_data: InputModel, string_transcription_result: str):
        md_text = f"""## Audio Transcription Result  \n
{string_transcription_result}  \n

## Args
**model_size**: {input_data.model_size.value}\n
"""
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }
