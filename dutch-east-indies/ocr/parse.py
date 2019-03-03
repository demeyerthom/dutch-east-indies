import json

import requests


def parse(filename, overlay=False, filetype="", api_key='helloworld', language='eng', scale=False):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param scale: autoscale the document
                    Defaults to False
    :param filetype: The file type. Leave emtpy for automatic inference
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
    :return: Result object
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'filetype': filetype,
               'scale': scale
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image', files={filename: f}, data=payload, )

    data = r.content.decode()

    parsed = json.loads(data)

    if parsed['IsErroredOnProcessing']:
        raise ValueError(parsed["ErrorMessage"])

    return parsed
