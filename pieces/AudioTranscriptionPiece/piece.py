from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import os
import openai


class AudioTranscriptionPiece(BasePiece):
    """
    This Piece uses the OpenAI API to extract text transcripts from audio.
    """
    
    def piece_function(self, input_model: InputModel):

        # Secrets are retrieved from ENV vars
        openai_api_key = os.environ.get("OPENAI_API_KEY", None)
        if openai_api_key is None:
            raise Exception("OPENAI_API_KEY not found in ENV vars. Please add it to the secrets section of the Piece.")
        openai.api_key = openai_api_key

        # Input arguments are retrieved from the Input model object
        file_path = input_model.file_path
        
        print("Making OpenAI audio transcription request...")
        try:
            audio_file = open(file_path, "rb")
            result = openai.Audio.transcribe(
                model="whisper-1", 
                file=audio_file,
                prompt=input_model.prompt,
                temperature=input_model.temperature
            )
        except Exception as e:
            print(f"\nTrascription task failed: {e}")
            raise Exception(f"Transcription task failed: {e}")
        finally:
            audio_file.close()
        
        if input_model.output_type == "xcom":
            self.logger.info("Transcription complete successfully. Result returned as XCom.")
            msg = f"Transcription complete successfully. Result returned as XCom."
            transcription_result = result
            output_file_path = ""
        else:
            self.logger.info("Transcription complete successfully. Result returned as file.")
            msg = f"Transcription complete successfully. Result returned as file."
            transcription_result = ""
            output_file_path = f"{self.results_path}/transcription_result.txt"
            with open(output_file_path, "w") as f:
                f.write(result)


        # Finally, results should return as an Output model
        return OutputModel(
            message=msg,
            transcription_result=transcription_result,
            file_path=output_file_path
        )