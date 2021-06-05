import smtplib
from email.message import EmailMessage
import speech_recognition as sr
import pyttsx3 as speaker
import details

recogniser = sr.Recognizer()
print(sr.Microphone.list_microphone_names())  # Your available microphone list
engine = speaker.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)  # female voice


# Function for sending mail
def send_mail():
    speak("Hi there, So you want to send a mail.")  # Greeting the user
    email = details.get_email()  # Your email id(Sender id)
    password = details.get_password()  # Your email password(Sender password)

    receiver = get_receiver_name()
    subject = get_subject()
    msg = get_message()
    # print("Your mail id:", email)
    print("Receiver mail id", receiver, "\n",
          "Subject:", subject, "\n",
          "message:", msg)

    # message format
    message = EmailMessage()
    message['From'] = email
    message['Subject'] = subject  # Subject
    message['To'] = receiver  # Receiver of the Mail
    message.set_content(msg)  # Email body or Content

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:  # Added SMTP Server
        smtp.login(email, password)  # Login into your account
        smtp.send_message(message)  # Sends your mail


# Function to let the computer speak
def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()


# To check whether the recognized speech is correct or not
def listening_checking():
    try:
        print("listening")
        with sr.Microphone() as source:
            recogniser.adjust_for_ambient_noise(source, duration=1)
            audio = recogniser.listen(source)
            speak("Let me recognise this")
            print("Let me recognise this...")
            text = recogniser.recognize_google(audio)
            print(text)
        return text
    except Exception as e:
        print(e)


# Function is going to listen to the speaker and
# Then use the google api to convert the speech to text format
def listen():
    try:
        print("listening")
        with sr.Microphone() as source:
            recogniser.adjust_for_ambient_noise(source, duration=2)
            audio = recogniser.listen(source)
            speak("Let me recognise this")
            print("Let me recognise this..")
            text = recogniser.recognize_google(audio)
            print(text)
        speak("Is it correct")
        if "yes" in listening_checking():  # Checking whether the recognized speech is correct or not
            return text.lower()
        else:
            speak("Let's try this again")
            text = listen()
            return text
    except Exception as e:
        print(e)


# Getting the subject for the mail
def get_subject():
    speak("What's your subject for this email")
    subject = listen()
    return subject


# Getting the message
def get_message():
    speak("Finally what's your content")
    message = listen()
    return message


# Getting the name of the receiver
def get_receiver_name():
    speak("To whom you want to send this email")
    name = listen()
    mail_id = verifying_receiver_name(name)
    if not mail_id:  # email not found
        speak("Sorry contact not found, Could you repeat again")
        mail_id = get_receiver_name()
        # return mail_id
    return mail_id


# Checking whether the receiver name is present in our contacts or not
def verifying_receiver_name(name):
    try:
        mail_id = details.contact_list[name]  # Getting the mail id from the contacts
        print("found")
        speak("Got it")
        return mail_id
    except:
        print("Not found")
        speak("Let me check once more")
        return 0


send_mail()  # Program starts here
