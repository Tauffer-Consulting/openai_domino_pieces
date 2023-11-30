from domino.testing import piece_dry_run
import os


def test_information_extraction_piece():
    input_text = "My name is John and I am 30 years old. I have 976,47 euros in my bank account."
    openai_model = "gpt-3.5-turbo-1106"
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
        },
        {
            "name": "money",
            "type": "float",
            "description": "Numeric value of the amount of money in the bank account."
        }
    ]

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    output = piece_dry_run(
        piece_name="InformationExtractionPiece",
        input_data={
            "input_text": input_text,
            "openai_model": openai_model,
            "extract_items": extract_items
        },
        secrets_data={
            "OPENAI_API_KEY": OPENAI_API_KEY
        }
    )

    assert output.get('name') == "John"
    assert output.get('age') == 30
    assert output.get('money') == 976.47
