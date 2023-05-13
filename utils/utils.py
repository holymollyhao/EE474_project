import openai
def set_openai():
    OPENAI_API_KEY = "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"
    openai.api_key = OPENAI_API_KEY
    model = "gpt-3.5-turbo"
    return model

def construct_message_playlist(hours:int, mood:str, genre:str):
    query = f"give me a {hours}-h {mood} playlist of {genre}"
    prompt_for_parsing = ", without additional responses attached on the front and back, just give me a list with numbering starting from 1"

    role = f"You are a music curator, who recommends music lists with consistent mood and genere"

    query += prompt_for_parsing
    messages = [
            {"role": "system", "content": role},
            {"role": "user", "content": query}
    ]
    return messages

def construct_message_image(mood:str, genre:str):
    query = f"Describe a scene where you might listen to a {mood} playlist of {genre}"
    prompt_for_parsing = ", without additional responses attached on the front and back, just give me a description of the surroundings, as descriptive as you can, but constrain your output to a maximum of 77 tokens"

    role = f"You are a assistant who generates prompts for image generation, who describes a likely scene based on the mood and genere of a music playlist"

    query += prompt_for_parsing
    messages = [
        {"role": "system", "content": role},
        {"role": "user", "content": query}
    ]
    return messages

def generate_response(model, message):
    response = openai.ChatCompletion.create(
        model=model,
        messages=message
    )
    return response['choices'][0]['message']['content']

