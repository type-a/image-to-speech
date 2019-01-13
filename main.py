import io
import os

def detect_document(path):
    """Detects document features in an image."""
    word_sent = ""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            # print('\nBlock confidence: {}\n'.format(block.confidence)) # this is for debug

            for paragraph in block.paragraphs:
                # print('Paragraph confidence: {}'.format(
                #     paragraph.confidence)) # this is for debug will be removed .....

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols 
                    ])
                    word_sent += " " + word_text
                    # print(word_text, end=" ") # for debug purpose will be removed later on 
    return word_sent

                    # for symbol in word.symbols:
                    #     print('\tSymbol: {} (confidence: {})'.format(
                    #         symbol.text, symbol.confidence))


def text2speech(text):
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(str(text))
    engine.setProperty('rate',70)
    engine.setProperty('volume',0.9) 
    engine.runAndWait()
    print("done ...")


def englishonly(text):
    from google.cloud import translate
    translate_client = translate.Client()
    target = 'en'
    translation = translate_client.translate(
    text,
    target_language=target)
    return translation['translatedText']


def image2speech(image):
    sent = englishonly(detect_document(image))
    # return sent
    conv_sent = englishonly(sent)
    text2speech(conv_sent)



image2speech("figure-66.jpg")


