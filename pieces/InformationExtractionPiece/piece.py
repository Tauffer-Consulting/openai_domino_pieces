from domino.base_piece import BasePiece
from .models import InputModel, OutputModel, SecretsModel
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain


class InformationExtractionPiece(BasePiece):  

    def piece_function(self, input_data: InputModel, secrets_data: SecretsModel):                
        # OpenAI settings
        if secrets_data.OPENAI_API_KEY is None:
            raise Exception("OPENAI_API_KEY not found in ENV vars. Please add it to the secrets section of the Piece.")

        llm = ChatOpenAI(
            openai_api_key=secrets_data.OPENAI_API_KEY,
            model=input_data.openai_model,
            temperature=0
        )
        schema = {
            "properties": {},
            "required": [],
        }
        for item in input_data.extract_items:
            schema["properties"][item.name] = {
                "type": item.type,
                "description": item.description,
            }
            schema["required"].append(item.name)
        chain = create_extraction_chain(schema, llm)

        # Run extraction chain
        self.logger.info(f"Running extraction chain")
        result = chain.run(input_data.input_text)

        # Display result in the Domino GUI
        self.format_display_result(input_data, result[0])

        # Return extracted information
        self.logger.info(f"Returning extracted information")
        return OutputModel(**result[0])
        

    def format_display_result(self, input_data: InputModel, result: dict):
        md_text = f"""## Extracted Information\n"""
        for item in input_data.extract_items:
            md_text += f"""### {item.name}:\n{result[item.name]}\n"""
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }
