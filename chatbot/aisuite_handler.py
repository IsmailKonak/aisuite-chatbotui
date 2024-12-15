import aisuite as ai
client = ai.Client()

def get_model_response(model, messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        # max_tokens=100
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content
