from domino.testing import piece_dry_run
import pytest


def run_piece(input_text: str, output_type):

    return piece_dry_run(
        #name of the piece
        piece_name="TextSummarizerPiece",

        #values to the InputModel arguments
        input_data={
            "input_text": input_text,
            "output_type": output_type,
        },
    )

@pytest.mark.skip(reason="Not implemented yet")
def test_text_summarizer_piece():
    output = run_piece(
        input_text=
"""Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.

The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.""",
        output_type="xcom",
    )

    assert "message" in output.keys()
    assert "summary_result" in output.keys()
    assert "file_path" in output.keys()