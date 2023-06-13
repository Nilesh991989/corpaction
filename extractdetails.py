import os
import PyPDF2
import docx
from docx.opc.constants import RELATIONSHIP_TYPE as RT
import re
import spacy

directory = 'C:/Users/Akshay/Downloads/accenture2904'
name_pattern = r"([A-Z][a-z]*\s+){1,2}[A-Z][a-z]*"
email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
phone_pattern = r"\b\d{10}\b"
nlp = spacy.load('en_core_web_sm')

def extractDetails(file, text):
    name_matches = re.findall(name_pattern, text)
    if len(name_matches) > 0:
        name = name_matches[0].strip()
    else:
        name = ""

    email_matches = re.findall(email_pattern, text)
    if len(email_matches) > 0:
        email = email_matches[0]
    else:
        email = ""

    phone_matches = re.findall(phone_pattern, text)
    if len(phone_matches) > 0:
        phone = phone_matches[0]
    else:
        phone = ""

    print(f"{file}, {name}, {phone}, {email}")


def processdocxfile(file):
    doc = docx.Document(directory + '/' + file)
    text = ''

    for para in doc.paragraphs:
        text = text + para.text
        text = text + "\n"

    extractDetails(file, text)


def processpdffile(file):
    reader = PyPDF2.PdfReader(directory + '/' + file)
    num_pages = len(reader.pages)
    text = ''
    for i in range(num_pages):
        page = reader.pages[i]
        extractedtext = page.extract_text()
        text = text + extractedtext
        text = text + '\n'

    extractDetails(file, text)

def readandprocessfiles():
    files = os.listdir(directory)
    for file in files:
        if ".docx" in file:
            processdocxfile(file)
        else:
            processpdffile(file)


if __name__ == "__main__":
    readandprocessfiles()