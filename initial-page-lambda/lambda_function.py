import os
import urllib
import openai
# from stable_diffusion import generate_image
# from chat_history import ChatHistory

openai.organization = os.environ['OPENAI_ORG']
openai.api_key = os.environ['OPENAI_KEY']

def lambda_handler(event, context):
    #get prompt from sender and hit openAPI with it
    prompt = urllib.parse.unquote(event['queryStringParameters']['prompt'], encoding='utf-8', errors='replace')
    prompt = prompt.replace("+", " ")

    image_response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = image_response['data'][0]['url']


    text_prompt = """
        generate some html content inside a div tag with a unique id. generate the content based on the following prompt: "%s" and incorporate the image at this url: "%s"
    """
    prompt = text_prompt % (prompt, image_url)
    text_response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        best_of=1
    )

    text_prompt_response = text_response["choices"][0]["text"]

    # code_prompt = """
    #     generate some html content inside a div tag with a unique id. generate the content based on the following prompt: "%s" and incorporate the image at this url: "%s"
    # """
    # code_prompt = code_prompt % (text_prompt_response, image_url)
    # code_response = openai.Completion.create(
    #     model="code-davinci-002",
    #     prompt=code_prompt,
    #     temperature=0,
    #     max_tokens=1000,
    #     top_p=0.1,
    #     frequency_penalty=0.0,
    #     presence_penalty=0.6,
    #     best_of=3,
    #     # stop=["\nHuman:", "\nAI:"]
    # )

    # code_response = code_response["choices"][0]["text"]

    # chatHistory = ChatHistory(client_number)
    # full_prompt = chatHistory.retrieve_append_chat(prompt)

    # chatHistory.update_chat_remote(full_prompt, prompt_response)


    return {
      "statusCode": 200,
      "headers": {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
      },
      "body": text_prompt_response
    }

if __name__ == "__main__":
    input_event = {
        'queryStringParameters' :{
            'prompt': 'puppy stuff'
        }
    }
    print(lambda_handler(input_event, {}))
