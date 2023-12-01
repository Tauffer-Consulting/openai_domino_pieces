from domino.testing import piece_dry_run
import os

def run_piece(
    prompt: str,
    image_format: str,
    output_type: str,
    size: str = "1024x1024",
):

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    return piece_dry_run(
        piece_name="ImageGeneratorPiece",
        input_data={
            "prompt": prompt,
            "image_format": image_format,
            "output_type": output_type,
            "size": size
        },
        secrets_data={
            "OPENAI_API_KEY": OPENAI_API_KEY
        }
)

def test_piece():
    piece_kwargs = {
        "prompt": "draw a punk art style painting",
        "image_format": "base64_string",
        "output_type": "file_and_string",
        "size": "512x512",
    }

    output = run_piece(
        **piece_kwargs
    )

    if piece_kwargs["image_format"] == "url":
        if piece_kwargs["output_type"] == "file":
            assert output.get('output_string') == None
            assert output.get('output_file_path').endswith(".txt")
        if piece_kwargs["output_type"] == "string":
            assert output.get('output_string') != None and type(output.get('output_string')) == str
            assert output.get('output_file_path') == None
        if piece_kwargs["output_type"] == "file_and_string":
            assert output.get('output_string') != None and type(output.get('output_string')) == str
            assert output.get('output_file_path').endswith(".txt")
    if piece_kwargs["image_format"] == "image_png":
        if piece_kwargs["output_type"] == "file":
            assert output.get('output_string') == None
            assert output.get('output_file_path').endswith(".png")
        if piece_kwargs["output_type"] == "string":
            assert output.get('output_string') == None
            assert output.get('output_file_path').endswith(".png")
        if piece_kwargs["output_type"] == "file_and_string":
            assert output.get('output_string') == None
            assert output.get('output_file_path').endswith(".png")
    if piece_kwargs["image_format"] == "base64_string":
        if piece_kwargs["output_type"] == "file":
            assert output.get('output_string') == None
            assert output.get('output_file_path').endswith(".txt")
        if piece_kwargs["output_type"] == "string":
            assert output.get('output_string') != None and type(output.get('output_string')) == str
            assert output.get('output_file_path') == None
        if piece_kwargs["output_type"] == "file_and_string":
            assert output.get('output_string') != None and type(output.get('output_string')) == str
            assert output.get('output_file_path').endswith(".txt")

