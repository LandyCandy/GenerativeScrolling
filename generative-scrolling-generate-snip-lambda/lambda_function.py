import os
import urllib
import openai
from stable_diffusion import generate_image
# from story_history import StoryHistory

openai.organization = os.environ['OPENAI_ORG']
openai.api_key = os.environ['OPENAI_KEY']

TEXT_PROMPT = """
    generate some html content inside a div tag with a unique id. generate the content as a new chapter in the following story: "%s"
"""

TEXT_IMAGE_PROMPT = """
    generate some html content inside a div tag with a unique id. generate the content as a new and unique continuation of the following story: "%s" and incorporate the image at this url: "%s"
"""

def lambda_handler(event, context):
    #get prompt from sender and hit openAPI with it
    prompt = urllib.parse.unquote(event['prompt'], encoding='utf-8', errors='replace')
    prompt = prompt.replace("+", " ")

    text_response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=1.0,
        presence_penalty=1.0
    )

    text_prompt_response = text_response["choices"][0]["text"]

    if 'image' in event and event['image']:
        image_url = generate_image(prompt, event['init_img'])
        prompt = TEXT_IMAGE_PROMPT % (text_prompt_response, image_url)
    else:
        prompt = TEXT_PROMPT % text_prompt_response

    html_response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )

    html_prompt_response = html_response["choices"][0]["text"]


    return {
      "statusCode": 200,
      "headers": {
        "Access-Control-Allow-Origin": "*"
      },
      "body": html_prompt_response
    }

if __name__ == "__main__":
    input_event = {
        'queryStringParameters' :{
            'prompt': 'puppy stuff'
        }
    }
    print(lambda_handler(input_event, {}))
