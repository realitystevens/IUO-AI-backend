import nltk
import os
import sys
import PyPDF2
import google.generativeai as genai
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

from dotenv import load_dotenv
load_dotenv()

nltk.download('punkt_tab')


class IUOAIproject:
    def __init__(self):
        """ Configure Gemini AI API """
        try:
            GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
            genai.configure(api_key=GOOGLE_API_KEY)
            self.model = genai.GenerativeModel("gemini-1.5-pro-latest")
            self.pdfText = ""
        except Exception as e:
            print(f"Initialization error: {e}")
            sys.exit(1)

    def extractPDFText(self, pdfPath):
        try:
            text = ""
            with open(pdfPath, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    pageText = page.extract_text()
                    if pageText:
                        text += "\n\n" + pageText
            return text
        except Exception as e:
            return f"Error extracting text from PDF: {e}"

    def loadPDF(self, pdfPath):
        """Validate if PDF file exists"""
        if not os.path.exists(pdfPath):
            print(f"Error: File {pdfPath} does not exist")

        """Set up extracted text from PDF"""
        self.pdfText = self.extractPDFText(pdfPath)
        if not self.pdfText:
            print("Failed to extract text from PDF file on loading the file")
            return False

        print(
            f"Successfully loaded PDF and extracted text. Total word count: {len(self.pdfText.split())}")
        return True

    def askQuestion(self, question):
        """Validate if PDF is loaded"""
        if not self.pdfText:
            return "Please load a PDF first using 'load [path to PDF]'"

        try:
            prompt = f"""
            You are an expert at extracting precise information from documents. 
            Use the following document text to answer the question as accurately as possible.
            If the answer is not in the document, say "I cannot find the answer in the provided document."

            Document Text:
            {self.pdfText}

            Question: {question}

            Answer:
            """

            response = self.model.generate_content(prompt)

            return response.text.strip()
        except Exception as e:
            return f"Error processing question: {e}"


def main():
    project = IUOAIproject()

    print(
        f"""
            Welcome to the IUO AI project script.
            Follow the instructions to proceed.

            Instructions:
                1. To proceed with the application, PDF must be loaded.
                    To load PDF, use the command keyword 'load [path to PDF]'.
                    For example: load IUO_prospectus_2016-2020.pdf

                2. After loading the PDF, use the command keyword 'ask' followed your question.
                    For example: ask what is the name of the Vice Chancellor

                3. To exit the application, use the command keyword 'exit'.
        """
    )

    while True:
        try:
            user_input = input("\n> ").strip()

            """Exit command"""
            if user_input.lower() == "exit":
                print("Exiting application")
                break

            """Load PDF command"""
            if user_input.lower().startswith("load "):
                pdfPath = user_input[5:].strip()
                if project.loadPDF(pdfPath):
                    print("PDF loaded successfully")
                continue

            """Ask question commmand"""
            if user_input.lower().startswith("ask "):
                question = user_input[4:].strip()
                if not question:
                    print("Please, provide a question")
                    continue

                """Get and print the answer"""
                answer = project.askQuestion(question)
                print("\nAnswer: ", answer)
                continue

            """Handle unrecognized command"""
            print("Unrecognized command. Please, follow the instruction above")

        except KeyboardInterrupt:
            print("\nOperation cancelled. Type 'exit' to quit")
        except Exception as e:
            print(f"An error occured: {e}")


if __name__ == "__main__":
    main()
