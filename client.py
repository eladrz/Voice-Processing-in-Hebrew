import speech_recognition as sr
from translate import Translator
import socket
import ast

# Set the server
ServerPort = 2224
# ServerIP = '192.168.1.125'
ServerIP = '192.168.68.226'
serverAddress = (ServerIP, ServerPort)
bufferSize = 1024
UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Obtain audio from the microphone
r = sr.Recognizer()


def dataFromServer(data):
    if data == '-1':
        print("error")
    elif len(data) == 3:
        if data[0] == '1':
            print("White led are on")
        if data[1] == '1':
            print("red led are on")
        if data[2] == '1':
            print("green led are on")
        if data[0] == '0':
            print("White led are off")
        if data[1] == '0':
            print("red led are off")
        if data[2] == '0':
            print("green led are off")


def manual():
    cmd = input("Input the command: ").lower()
    # Send it to the server
    cmd = cmd.encode('utf-8')
    UDPClient.sendto(cmd, serverAddress)
    # Get data from the server
    data, address = UDPClient.recvfrom(bufferSize)
    data = data.decode('utf-8')
    dataW = ast.literal_eval(data)
    dataFromServer(dataW)


# Recognize speech using Whisper
while True:
    try:
        check = input("Are you want to say the command(yes or no)?")
        if check == 'yes' or check == 'y':
            # lessen to the microphone
            with sr.Microphone() as source:
                print("Hello what is your command in Hebrew")
                audio = r.listen(source)
                print("Processing...")
                data = r.recognize_whisper(audio, language="he")
            print("Whisper thinks you said: " + data)

            # Translate the recognized text from Hebrew to English
            translator = Translator(to_lang="en", from_lang="he")
            translated_text = translator.translate(data)
            # print("Translated text: " + translated_text)
            translated_text = translated_text.lower()
            # Send it to the server
            translated_text = translated_text.encode('utf-8')
            UDPClient.sendto(translated_text, serverAddress)

            # Get data from the server
            data, address = UDPClient.recvfrom(bufferSize)
            data = data.decode('utf-8')
            # print(data)
            dataFromServer(data)
        else:
            manual()

    except sr.UnknownValueError:
        print("Whisper could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper")
