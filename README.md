# GenerativeScrolling

Objective:
Create a novel (textual + graphic) interface connected to a backend that, upon scrolling to the bottom of the initial html page, is called. 
The backend uses a Transformer model to generate a new section of html code with generated content inside that is then appended to the end of the
calling html page.

## Possible backend stack: 
- Route 53
- API Gateway
- Lambda Function (one to serve initial (or stored) HTML page, one to generate new content)
   - OpenAI code generation model
   - OpenAI Gpt3 Text Generator
   - OpenAI or Stable Diffusion Image generator
   - Python html validator
- S3 (to store previous pages)

## Possible frontend stack:
TBA (to be augusto'd)
