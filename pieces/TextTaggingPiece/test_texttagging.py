from domino.testing import piece_dry_run
import os


def test_texttagging():
    input_text = "Estoy increiblemente contento de haberte conocido! Creo que seremos muy buenos amigos!"
    openai_model = "gpt-3.5-turbo-1106"
    tags = [
        {
            "name": "sentiment_score",
            "type": "float",
            "description": "Sentiment score of the text. Should be a number between -1 and 1."
        },
        {
            "name": "sentiment",
            "type": "string",
            "description": "Sentiment of the text.",
            "enum": "anger,sad,neutral,happy,joy"
        },
        {
            "name": "language",
            "type": "string",
            "description": "Language of the text."
        },
    ]

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if OPENAI_API_KEY is None:
        raise Exception("OPENAI_API_KEY not found in ENV vars.")

    output = piece_dry_run(
        piece_name="TextTaggingPiece",
        input_data={
            "input_text": input_text,
            "openai_model": openai_model,
            "tags": tags
        },
        secrets_data={
            "OPENAI_API_KEY": OPENAI_API_KEY
        }
    )

    assert output.get("sentiment_score") is not None
    assert output.get("sentiment_score") > 0
    assert output.get("sentiment") is not None
    assert output.get("sentiment") == "happy"
    assert output.get("language") is not None
    assert output.get("language") in ["Spanish", "spanish"]
