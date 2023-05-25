from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import os
import openai
from pydub import AudioSegment


class AudioTranscriptionPiece(BasePiece):
    """
    This Piece uses the OpenAI API to extract text transcripts from audio.
    """
    def piece_function(self, input_model: InputModel):
        openai_api_key = self.secrets.OPENAI_API_KEY
        if openai_api_key is None:
            raise Exception("OPENAI_API_KEY not found in ENV vars. Please add it to the secrets section of the Piece.")
        openai.api_key = openai_api_key

        # Input arguments are retrieved from the Input model object
        file_path = input_model.audio_file_path
        
        print("Making OpenAI audio transcription request...")
        try:
            full_audio = AudioSegment.from_mp3(file_path)
            total_time = len(full_audio)
            # PyDub handles time in milliseconds
            ten_minutes = 10 * 60 * 1000
            full_transcript = ""
            i = 0
            while True:
                # Split audio into 10 minute chunks, run transcription on each chunk
                print(f"Transcribing audio chunk {i+1}...")
                endpoint = min((i+1)*ten_minutes, total_time-1)
                minutes = full_audio[i*ten_minutes:endpoint]
                minutes.export(f"audio_piece_{i}.mp3", format="mp3")
                audio_file= open(f"audio_piece_{i}.mp3", "rb")
                transcript = openai.Audio.transcribe(
                    model="whisper-1", 
                    file=audio_file,
                    temperature=input_model.temperature
                ).to_dict()["text"]
                full_transcript += " " + transcript
                i += 1
                audio_file.close()
                if endpoint == total_time-1:
                    break
        except Exception as e:
            print(f"\nTrascription task failed: {e}")
            raise Exception(f"Transcription task failed: {e}")

        # Display result in the Domino GUI
        self.format_display_result(input_model=input_model, string_transcription_result=full_transcript)
        
        if input_model.output_type == "string":
            self.logger.info("Transcription complete successfully. Result returned as string.")
            msg = f"Transcription complete successfully. Result returned as string."
            return OutputModel(
                message=msg,
                string_transcription_result=full_transcript
            )
                
        output_file_path = f"{self.results_path}/{input_model.output_file_name}"
        with open(output_file_path, "w") as f:
            f.write(full_transcript)

        if input_model.output_type == "file":
            self.logger.info(f"Transcription complete successfully. Result returned as file in {output_file_path}")
            msg = f"Transcription complete successfully. Result returned as file."
            return OutputModel(
                message=msg,
                file_path_transcription_result=output_file_path
            )

        self.logger.info(f"Transcription complete successfully. Result returned as string and file in {output_file_path}")
        msg = f"Transcription complete successfully. Result returned as string and file."
        return OutputModel(
            message=msg,
            string_transcription_result=full_transcript,
            file_path_transcription_result=output_file_path
        )
    
    def format_display_result(self, input_model: InputModel, string_transcription_result: str):
        md_text = f"""
## Generated transcription:  \n
{string_transcription_result}  \n

## Args
**temperature**: {input_model.temperature}
"""
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }