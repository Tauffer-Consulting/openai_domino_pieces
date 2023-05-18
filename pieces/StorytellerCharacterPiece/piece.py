from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import openai

class StorytellerCharacterPiece(BasePiece):
    def openai_response(self, input_model: InputModel, prompt: str, temperature: float = None):
        # Input arguments
        openai_model = input_model.openai_model
        completion_max_tokens = input_model.completion_max_tokens

        try:
            if openai_model in ["gpt-3.5-turbo", "gpt-4"]:
                response = openai.ChatCompletion.create(
                    model=openai_model,
                    messages = [
                        {"role": "user", "content": prompt}
                    ],
                    temperature=input_model.temperature if temperature is None else temperature,
                    max_tokens=completion_max_tokens,
                )
                return response['choices'][0]['message']['content']
            else:
                response = openai.Completion.create(
                    model=openai_model,
                    prompt=prompt,
                    temperature=input_model.temperature if temperature is None else temperature,
                    max_tokens=completion_max_tokens,
                )
                r_dict = response.to_dict_recursive()
                return r_dict["choices"][0]["text"]
        except Exception as e:
            self.logger.info(f"\nCompletion task failed: {e}")
            raise Exception(f"Completion task failed: {e}")  
    
    def summarize_previous_stories(self, input_model: InputModel, previous_stories: str):
        prompt = f"""Write a summary of the stories below.
Write as if you were telling this summary to the character themselves.
The name of the character is {input_model.character_name}.
Stories:
{previous_stories}"""
        return self.openai_response(input_model, prompt, temperature=0.3)
        
    def piece_function(self, input_model: InputModel):
        storyteller_template = """You are a storyteller. You love to tell stories based on your experiences and your life. 
You are very creative and your stories are so different from each other. Your stories vary in telling about love, adventure, sadness, challenges, overcoming, comic events, dramas, comedies, action, romance and sensuality.
You also talk about your family, your friends and your loved ones.
Many times, you mix these characteristics together to tell your story.
Your name is {name}.
Your description is: {description}

{previous_stories_summary}

Now tell us a new story of yours.
Attention, tell the story as if you were {name}, narrate it in the first person.
You can imagine whetever you want to create a new story!
Begin of your new story:
"""
        openai.api_key = self.secrets.OPENAI_API_KEY
        character_name = input_model.character_name
        character_description = input_model.character_description
        if input_model.previous_stories_file_path:
            all_stories = open(input_model.previous_stories_file_path).read()
            summary = self.summarize_previous_stories(input_model, all_stories)
            previous_stories_summary = f"You have already told some stories. Here is a summary of them:\n{summary}"
            prompt = storyteller_template.format(name=character_name, description=character_description, previous_stories_summary=previous_stories_summary)
            new_story = self.openai_response(input_model, prompt).replace("\n\n", "\n")
            all_stories += f"Begin of a story:\n{new_story}\nEnd of a story\n"
            output_file_path = input_model.previous_stories_file_path
        else:
            prompt = storyteller_template.format(name=character_name, description=character_description, previous_stories_summary="")
            new_story = self.openai_response(input_model, prompt).replace("\n\n", "\n")
            all_stories = f"""
These all stories are told by {character_name}.
The description of {character_name}: {character_description}.\n
Begin of a story:\n{new_story}\nEnd of a story\n"""
            output_file_path = f"{self.results_path}/all_stories_from_{character_name}.txt"

        new_story_with_character_info = f"""
This is a story told by: {character_name}
The description of {character_name}: {character_description}
The story: {new_story} """

        with open(output_file_path, "w") as f:
            f.write(all_stories)

        # Display result in the Domino GUI
        self.format_display_result(input_model, new_story)

        return OutputModel(
            new_story=new_story,
            new_story_with_character_info=new_story_with_character_info,
            stories_file_path=output_file_path
        )
    
    def format_display_result(self, input_model: InputModel, new_story: str):
        md_text = f"""
## New story
{new_story}

## Args
**character name**: {input_model.character_name}
**character description**: {input_model.character_description}
**model**: {input_model.openai_model}
**temperature**: {input_model.temperature}
**max_tokens**: {input_model.completion_max_tokens}
"""
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }