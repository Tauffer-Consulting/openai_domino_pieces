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
        
        # Prepare output based on the output type
        if input_model.output_type == "string":
            self.logger.info("Transcription complete successfully. Result returned as string.")
            msg = f"Transcription complete successfully. Result returned as string."
            transcription_result = full_transcript
        else:          
            #getting the file name without the extension
            file_name, ext = os.path.splitext(os.path.basename(input_model.audio_file_path)) 
            #getting the directory path
            dir_path = os.path.dirname(input_model.audio_file_path) 

            output_file_path = f"{dir_path}/{file_name}_transcription_result.txt"
            self.logger.info(f"Transcription complete successfully. Result returned as file in {output_file_path}")
            msg = f"Transcription complete successfully. Result returned as file."
            transcription_result = output_file_path
            with open(output_file_path, "w") as f:
                f.write(full_transcript)

        # Finally, results should return as an Output model
        return OutputModel(
            message=msg,
            transcription_result=transcription_result,
        )