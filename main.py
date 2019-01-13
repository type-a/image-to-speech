import io
import os
import subprocess

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


def text2mp3(text):
    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.types.SynthesisInput(text=text)
    voice = texttospeech.types.VoiceSelectionParams(
    language_code='en-US',
    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    with open('output.mp3', 'wb') as out:
    # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')




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
    text2mp3(conv_sent)

def music2speech(path):
    subprocess.Popen(['omxplayer', path])
    

image2speech("figure-68.jpeg")
