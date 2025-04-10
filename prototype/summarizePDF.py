"""
    Summarize the content of the PDF file 
    using a natural language processing library
    and save the summarized text to a new file 
    called 'summarized_IUO_prospectus_2016-2020.txt'
"""
import os
import PyPDF2
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "IUO_prospectus_2016-2020.pdf")


def extractPDFtext(pdfPath):
    try:
        text = ""
        with open(pdfPath, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                pageText = page.extract_text()
                if pageText:
                    text += "\n\n" + pageText

        word_count = len(text.split())
        print(f"Text extracted successfully. Word count: {word_count}")
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def summarize(text, num_sentences=200):
    # Check if the nltk punkt tokenizer is already downloaded
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    print(f"Summarized text to {num_sentences} sentences")

    return " ".join(str(sentence) for sentence in summary)


if not os.path.exists(PDF_PATH):
    print(f"PDF file not found: {PDF_PATH}")
    exit(1)

text = extractPDFtext(PDF_PATH)
summarized_text = summarize(text, num_sentences=50)

output_filepath = os.path.join(
    BASE_DIR, "..", "summarized_IUO_prospectus_2016-2020.txt")

with open(output_filepath, "w") as file:
    file.write(summarized_text)

print("Successful. Summarized text saved to 'summarized_IUO_prospectus_2016-2020.txt'")
