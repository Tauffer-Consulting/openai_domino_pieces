from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from transformers import pipeline
import torch


def summarize_long_text(text: str, summarizer, iteration: int=0):
    """
    Generate the summary by concatenating the summaries of the individual chunks.
    """
    iteration += 1
    print(f"Iteration: {iteration}")

    # Preprocess text
    text = text.lower().replace(".", " ").replace(",", " ").replace("\n", " ")
    text = "".join(ch if ch.isalnum() or ch == " " else " " for ch in text)

    # Split the input text into chunks
    chunk_size = 1000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    print(f"chunks to process: {len(chunks)}")

    # Generate the summary for each chunk
    summary_list = [
        summarizer(chunk, max_length=60, min_length=30, no_repeat_ngram_size=3)[0]['summary_text']
        for chunk in chunks
    ]
    summary = " ".join(summary_list)

    if len(summary) > 2000:
        return summarize_long_text(summary, summarizer, iteration)
    else:
        return summary


class TextSummarizerLocalPiece(BasePiece):

    def piece_function(self, input_data: InputModel):

        # Set device
        if input_data.use_gpu and torch.cuda.is_available():
            device = torch.cuda.current_device()
            self.logger.info("Using GPU for inference.")
        else:
            device = -1
            self.logger.info("Using CPU for inference.")

        # Load text
        if input_data.input_file_path:
            with open(input_data.input_file_path, "r") as f:
                text_str = f.read()
        else:
            text_str = input_data.input_text

        # Load summarizer
        self.logger.info("Loading summarizer...")
        summarizer = pipeline(
            task="summarization",
            model="facebook/bart-large-cnn",
            framework="pt",
            device=device
        )

        # Run summarizer
        self.logger.info("Running summarizer...")
        result = summarize_long_text(text=text_str, summarizer=summarizer)

        # Return result
        if input_data.output_type == "xcom":
            self.logger.info("Summarization completed successfully. Result returned as XCom.")
            msg = f"Summarization completed successfully. Result returned as XCom."
            summary_result = result
            output_file_path = ""
        else:
            self.logger.info("Sumamrization completed successfully. Result returned as file.")
            msg = f"Summarization completed successfully. Result returned as file."
            summary_result = ""
            output_file_path = "summary_result.txt"
            with open(output_file_path, "w") as f:
                f.write(result)

        return OutputModel(
            message=msg,
            summary_result=summary_result,
            file_path=output_file_path
        )