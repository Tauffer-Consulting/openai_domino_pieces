from domino.scripts.piece_dry_run import piece_dry_run
import os


input_text = "My name is John and I am 30 years old."
openai_model = "gpt-3.5-turbo-0613"
extract_items = [
    {
        "name": "name",
        "type": "string",
        "description": "Name of the person."
    },
    {
        "name": "age",
        "type": "integer",
        "description": "Age of the person."
    }
]

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

output = piece_dry_run(
    repository_folder_path="../",
    piece_name="InformationExtractionPiece",
    piece_input={
        "input_text": input_text,
        "openai_model": openai_model,
        "extract_items": extract_items
    },
    secret_input={
        "OPENAI_API_KEY": OPENAI_API_KEY
    }
)

assert output["name"] == "John"
assert output["age"] == 30