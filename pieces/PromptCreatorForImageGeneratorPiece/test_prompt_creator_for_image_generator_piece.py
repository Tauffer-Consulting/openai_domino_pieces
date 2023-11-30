from domino.testing import piece_dry_run, skip_envs
import tiktoken
import os



def run_piece(
        context: str,
        art_style: str,
        output_type: str,
        completion_max_tokens: int,
        openai_model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
):

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    return piece_dry_run(
        piece_name="PromptCreatorForImageGeneratorPiece",
        input_data={
            "context": context,
            "art_style": art_style,
            "completion_max_tokens": completion_max_tokens,
            "output_type": output_type,
            "openai_model": openai_model,
            "temperature": temperature
        },
        secrets_data={
            "OPENAI_API_KEY": OPENAI_API_KEY
        }
)


@skip_envs('github')
def test_prompt_creator_for_image_generator_piece():
    piece_kwargs = {
        "context": "Explorers dive into a mesmerizing underwater city, discovering ancient secrets, mysterious symbols, and evidence of an advanced civilization.",
        "art_style": "surrealistic oceanic exploration",
        "completion_max_tokens": 350,
        "output_type": "file_and_string",
        "openai_model": "gpt-3.5-turbo",
        "temperature": 0.7,
    }

    output = run_piece(
        **piece_kwargs
    )

    if piece_kwargs["output_type"] == "file":
        assert output.get("generated_prompt_string") == None
        assert output.get("generated_prompt_file_path").endswith(".txt")
        generated_prompt_path = output.get("generated_prompt_file_path")
        with open(generated_prompt_path, "r") as f:
            generated_prompt = f.read()

    if piece_kwargs["output_type"] == "string":
        assert output.get("generated_prompt_string") != None and type(output.get("generated_prompt_string")) == str
        assert output.get("generated_prompt_file_path") == None
        generated_prompt = output.get("generated_prompt_string")
    if piece_kwargs["output_type"] == "file_and_string":
        assert output.get("generated_prompt_string") != None and type(output.get("generated_prompt_string")) == str
        assert output.get("generated_prompt_file_path").endswith(".txt")
        generated_prompt = output.get("generated_prompt_string")

    encoding = tiktoken.encoding_for_model(piece_kwargs["openai_model"])
    text_tokens = encoding.encode(text=generated_prompt)
    assert len(text_tokens) <= piece_kwargs["completion_max_tokens"]


