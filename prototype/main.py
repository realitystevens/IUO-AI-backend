"""
    Prototype of the project showing product's architecture and workflow.
    Run file on command line to see workflow and functionality
"""

import os
import sys
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

import nltk
nltk.download('punkt_tab')


class IUOAIproject:
    def __init__(self):
        """ Configure Gemini AI API """
        try:
            GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
            genai.configure(api_key=GOOGLE_API_KEY)
            self.model = genai.GenerativeModel("gemini-1.5-pro-latest")
            self.fileText = ""
        except Exception as e:
            print(f"Initialization error: {e}")
            sys.exit(1)

    def extractText(self, filePath):
        try:
            with open(filePath, "r", encoding="utf-8") as file:
                text = file.read()
            return text
        except Exception as e:
            return f"Error accessing TXT file: {e}"


    def askQuestion(self, question):
        self.fileText = self.extractText("summarized_IUO_prospectus_2016-2020.txt")
        if not self.fileText:
            return "Failed to extract text from TXT file"

        try:
            prompt = f"""
            You are an expert at extracting precise information from documents. 
            Use the following document text to answer the question as accurately as possible.
            If the answer is not in the document, say "I cannot find the answer in the provided document."

            Document Text:
            {self.fileText}

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
                1. To proceed with the application, 
                    use the command keyword 'ask', followed your question.
                    For example: ask what is the name of the Vice Chancellor

                2. To exit the application, use the command keyword 'exit'.
        """
    )

    while True:
        try:
            user_input = input("\n> ").strip()

            """Exit command"""
            if user_input.lower() == "exit":
                print("Exiting application")
                break

            if user_input.lower() == "ask" or user_input.lower() == "ask ":
                print("Please, provide a question")
                continue

            """Ask question commmand"""
            if user_input.lower().startswith("ask "):
                question = user_input[4:].strip()

                """Get and print the answer"""
                print("Processing question...")
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
