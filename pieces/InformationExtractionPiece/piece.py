from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from enum import Enum
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain


class TextSummarizerPiece(BasePiece):  

    def piece_function(self, input_model: InputModel):                
        # OpenAI settings
        if self.secrets.OPENAI_API_KEY is None:
            raise Exception("OPENAI_API_KEY not found in ENV vars. Please add it to the secrets section of the Piece.")

        llm = ChatOpenAI(
            openai_api_key=self.secrets.OPENAI_API_KEY,
            model=input_model.openai_model,
            temperature=0
        )
        schema = {
            "properties": {},
            "required": [],
        }
        for item in input_model.extract_items:
            schema["properties"][item.name] = {
                "type": item.type,
                "description": item.description,
            }
            schema["required"].append(item)
        chain = create_extraction_chain(schema, llm)

        # Run extraction chain
        self.logger.info(f"Running extraction chain")
        result = chain.run(input_model.input_text)

        # Display result in the Domino GUI
        self.format_display_result(input_model, result[0])

        # Return extracted information
        self.logger.info(f"Returning extracted information")
        return OutputModel(**result[0])
        

    def format_display_result(self, input_model: InputModel, result: dict):
        md_text = f"""## Extracted Information\n"""
        for item in input_model.extract_items:
            md_text += f"""### {item.name}:\n{result[item.name]}\n"""
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }
