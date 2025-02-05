"""
    Summarize the content of the PDF file 
    using a natural language processing library
    and save the summarized text to a new file 
    called 'summarized_IUO_prospectus_2016-2020.txt'
"""

import PyPDF2
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

import nltk
nltk.download('punkt_tab')





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
        success_message = f"Text extracted successfully. Word count: {word_count}"
        print(success_message)
        return text
    except Exception as e:
        error_message = f"Error extracting text from PDF: {e}"
        print(error_message)
        return ""


def summarize(text, num_sentences=200):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    print(f"Summarized text to {num_sentences} sentences")

    return " ".join(str(sentence) for sentence in summary)



text = extractPDFtext("IUO_prospectus_2016-2020.pdf")

summarized_text = summarize(text, num_sentences=50)


with open("summarized_IUO_prospectus_2016-2020.txt", "w") as file:
    file.write(summarized_text)

print("Successful. Summarized text saved to 'summarized_IUO_prospectus_2016-2020.txt'")
