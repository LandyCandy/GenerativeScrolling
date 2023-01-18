import codecs

def lambda_handler(event, context):
    infinite_scroll_page_file = codecs.open("infinite_scroll.html", 'r')
    infinite_scroll_page_string = infinite_scroll_page_file.read()

    response = {
      "statusCode": 200,
      'headers': {
        'Access-Control-Allow-Origin    ': '*',
      },
      "body": infinite_scroll_page_string
    }

    return response
