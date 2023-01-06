import boto3
from botocore.exceptions import ClientError

class StoryHistory:

    INIT_PROMPT = ("The following is a conversation with an AI assistant.\n" +
        "The assistant is very snarky, helpful, creative, clever and funny.\n" +
        "Human: Hello, who are you?\n" +
        "AI: Hello Meatbag. I am an AI named Shatbot. How can I be of moderate help to you today?\n")

    APPEND_PROMPT = "Human: %s\nAI: "

    BUCKET_NAME = 'myshitbucket'

    def __init__(self, phone_number):
        self.s3 = boto3.client('s3')
        self.file_name = phone_number + '.txt'
        self.file_key = 'story_history/' + self.file_name

    def retrieve_append_story(self, prompt, force_reset=False):
        #check if file exists
            #if yes:
                #retrieve file text, append prompt and return
            #if no or force_reset is True:
                #append prompt to init_prompt and return
        story_history = ''
        try:
            data = self.s3.get_object(Bucket=self.BUCKET_NAME, Key=self.file_key)
            contents = data['Body'].read()
            story_history = contents.decode("utf-8")
        except Exception:
            story_history = self.INIT_PROMPT
            pass

        if force_reset:
            story_history = self.INIT_PROMPT

        story_text = story_history + (self.APPEND_PROMPT % prompt)

        return story_text

    def update_story_remote(self, story_history, response):
        #dump story_history into self.file_name
        #upload to s3, default replacing if already present

        full_story_history = f"{story_history}{response}\n"

        try:
            self.s3.put_object(
                Body=full_story_history,
                Bucket=self.BUCKET_NAME,
                Key=self.file_key,
                ACL='public-read',
                ContentType='text/plain'
            )
        except ClientError as e:
            logging.error(e)

if __name__ == "__main__":
    storyHistory = StoryHistory("+213654")
    full_test_prompt = storyHistory.retrieve_append_story("Bananas")
    # full_test_prompt = storyHstoryHistoryistory.retrieve_append_story("Bananas", True)
    storyHistory.update_story_remote(full_test_prompt, "Are Bananas!")