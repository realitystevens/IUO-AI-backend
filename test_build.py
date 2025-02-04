import nltk
import os
import PyPDF2
import google.generativeai as genai
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


from dotenv import load_dotenv
load_dotenv()

nltk.download('punkt_tab')

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

pdfPath = "IUO_prospectus_2016-2020.pdf"

try:
    text = ""
    with open(pdfPath, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            pageText = page.extract_text()
            if pageText:
                text += "\n\n" + pageText

    print("Text extracted successfully")
    word_count = len(text.split())
    print(f"Word count: {word_count}")
except Exception as e:
    print(f"Error extracting text from PDF: {e}")


def summarize(text, num_sentences=200):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)

    return " ".join(str(sentence) for sentence in summary)


summarized_text = summarize(text, num_sentences=28600)

with open("summarized_IUO_prospectus_2016-2020.txt", "w") as file:
    file.write(summarized_text)

print("Successful. Summarized text saved to 'summarized_IUO_prospectus_2016-2020.txt'")
