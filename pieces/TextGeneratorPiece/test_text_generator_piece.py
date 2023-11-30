from domino.testing import piece_dry_run
from typing import List
import tiktoken
import os


def run_piece(
       template: str,
       prompt_args: List[dict],
       output_type: str,
       openai_model: str,
       completion_max_tokens: int,
       temperature: float = 0.3
):

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    return piece_dry_run(
        piece_name="TextGeneratorPiece",
        input_data={
            "template": template,
            "prompt_args": prompt_args,
            "output_type": output_type,
            "completion_max_tokens": completion_max_tokens,
            "openai_model": openai_model,
            "temperature": temperature,
        },
        secrets_data={
            "OPENAI_API_KEY": OPENAI_API_KEY
        }
)



def test_text_generator_piece():
    template = "tell me about the history of {event_history}"
    prompt_args = [{"arg_name": "event_history", "arg_value": "artifical intelligence"}]

    piece_kwargs = {
        "template": template,
        "prompt_args": prompt_args,
        "output_type": "file_and_string",
        "completion_max_tokens": 500,
        "openai_model": "gpt-3.5-turbo",
    }

    output = run_piece(
        **piece_kwargs
    )

    if piece_kwargs["output_type"] == "file":
        assert output.get("string_generated_text") == None
        assert output.get("file_path_generated_text").endswith(".txt")
    if piece_kwargs["output_type"] == "string":
        assert output.get("string_generated_text") != None and type(output.get("string_generated_text")) == str
        assert output.get("file_path_generated_text") == None
        generated_prompt = output.get("string_generated_text")
    if piece_kwargs["output_type"] == "file_and_string":
        assert output.get("string_generated_text") != None and type(output.get("string_generated_text")) == str
        assert output.get("file_path_generated_text").endswith(".txt")
        generated_prompt = output.get("string_generated_text")

    encoding = tiktoken.encoding_for_model(piece_kwargs["openai_model"])
    text_tokens = encoding.encode(text=generated_prompt)
    assert len(text_tokens) <= piece_kwargs["completion_max_tokens"]

