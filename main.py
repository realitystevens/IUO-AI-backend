import os
import sys
import PyPDF2
from decouple import config
import google.generativeai as genai


class IUOAIproject:
    def __init__(self):
        """ Configure Gemini AI API """
        try:
            GEMINI_APIKEY = config(
                "GEMINI_APIKEY") or os.getenv("GEMINI_APIKEY")
            if not GEMINI_APIKEY:
                raise ValueError(
                    "Gemini API Key not found. Please set GEMINI_APIKEY in .env file")

            genai.configure(api_key=GEMINI_APIKEY)

            """ Initialize the model """
            self.model = genai.GenerativeModel("gemini-1.5-pro-latest")
            self.pdfText = ""
        except Exception as e:
            print(f"Initialization error: {e}")
            sys.exit(1)

    def extractText(self, pdfPath):
        """
        Extract text from PDF file.

        Args:
            pdfPath (str): Path to PDF file

        Returns:
            str: Extracted text from PDF file
        """
        try:
            text = ""
            with open(pdfPath, "rb") as file:
                reader = PyPDF2.PdfReader(file)

                for page in reader.pages:
                    pageText = page.extract_text()

                    if pageText:
                        text += pageText + "\n\n"
            return text
        except Exception as e:
            errorMessage = f"Error extracting text from PDF: {e}"
            print(errorMessage)

            return errorMessage

    def loadPDF(self, pdfPath):
        """
        Load and process a PDF file

        Args:
            pdfPath (str): Path to the PDF file
        """
        # Validate if PDF file exists
        if not os.path.exists(pdfPath):
            print(f"Error: File {pdfPath} does not exist")

        # Set up extracted text
        self.pdfText = self.extractText(pdfPath)

        # Check if text extraction was successful
        if not self.pdfText:
            print("Failed to extract text from PDF file on loading the file")
            return False

        print(
            f"Successfully loaded PDF and extracted text. Total characters: {len(self.pdfText)}")
        return True

    def askQuestion(self, question):
        """
        Ask a question about the loaded PDF

        Args:
            question (str): Question to ask

        Returns:
            str: Answer from the AI
        """
        # Validate if PDF is loaded
        if not self.pdfText:
            return "Please load a PDF first using 'load [path to PDF]'"

        try:
            # Prepare the prompt
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
    """ Create an instance of the class 'IUOAIproject' """
    project = IUOAIproject()

    message = f"""
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

    print(message)

    while True:
        try:
            user_input = input("\n> ").strip()

            # Exit command
            if user_input.lower() == "exit":
                print("Exiting application")
                break

            # Load PDF command
            if user_input.lower().startswith("load "):
                pdfPath = user_input[5:].strip()
                if project.loadPDF(pdfPath):
                    print("PDF loaded successfully")
                continue

            # Ask question commmand
            if user_input.lower().startswith("ask "):
                question = user_input[4:].strip()
                if not question:
                    print("Please, provide a question")
                    continue

                # Get and print the answer
                answer = project.askQuestion(question)
                print("\nAnswer: ", answer)
                continue

            # Handle unrecognized command
            print("Unrecognized command. Please, follow the instruction above")

        except KeyboardInterrupt:
            print("\nOperation cancelled. Type 'exit' to quit")
        except Exception as e:
            print(f"An error occured: {e}")



if __name__ == "__main__":
    main()


# tokenizers = {
#     "GPT-3": 1.4,    # OpenAI's model
#     "BERT": 1.2,     # Google's BERT
#     "Gemini": 1.3,   # Google's Gemini
#     "Claude": 1.25   # Anthropic's model
# }


# def chunkText(text, max_token=8000):
#     """
#     Split long text into chunks that fits within Gemini's token limits

#     Args:
#         text (str): user_input text to chunk
#         max_tokens (str): Maximum token per chunks
#     """
#     words = text.split()
#     chunks = []
#     current_chunk = []
#     current_length = 0

#     for word in words:
#         # Rough token estimation (1 word ≈ 1.3 tokens)
#         word_token = len(word) * tokenizers["Gemini"]

#         if current_length + word_token > max_token:
#             chunks.append(" ".join(current_chunk))
#             current_chunk = []
#             current_length = 0

#         current_chunk.append(word)
#         current_length += word_token

#         if current_chunk:
#             chunks.append(" ".join(current_chunk))

#     return chunks


# print("Extracting text from PDF file...", extractText("IUO_prospectus_2016-2020.pdf"))
# print("Chunking the file...", chunkText(extractText("IUO_prospectus_2016-2020.pdf")))
