import os
from fastapi import FastAPI
from pydantic import BaseModel
from utils import getAnswer

from dotenv import load_dotenv
load_dotenv()




app = FastAPI(
    title = "IUO AI API",
    description = "Ask any question concerning Igbinedion University and get answers to the question.",
    version = "1.0.0",
    terms_of_service = "https://yourwebsite.com/terms",
    contact = {
        "name": "Google Developer Student Club, Igbinedion University Okada",
        "url": "https://linktr.ee/gdsciuo",
        "email": "gdsciuo@gmail.com"
    },
    license_info = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    docs_url = "/docs",
    redoc_url = "/docs/v2",
    root_path = "/",
    root_path_in_servers = True,
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class MessageSchema(BaseModel):
    question: str



@app.post("/api/v1/", tags=["AI"])
async def ask_AI(message: MessageSchema):
    """
    Handles AI-based question answering by reading a document, processing the question, 
    and returning the answer.

    Args:
        message (MessageSchema): An object containing the question to be answered.

    Returns:
        dict: A dictionary containing:
            - "question" (str): The input question.
            - "result" (str): The answer to the question, if found.
            - "status_code" (int): The status code indicating the result of the operation.
            - "error" (str, optional): An error message if the document is not found or 
              an exception occurs during processing.

    Raises:
        FileNotFoundError: If the specified document file is not found.
        Exception: For any other errors encountered while reading the document.
    """

    document_path = os.path.join(BASE_DIR, "summarized_IUO_prospectus_2016-2020.txt")
    
    try:
        with open(document_path, "r", encoding="utf-8") as file:
            document_content = file.read()
    except FileNotFoundError:
        return {"error": "Document not found."}
    except Exception as e:
        return {"error": f"Error reading document: {e}"}
    
    question = message.question

    result = getAnswer(document_content, question) #Note: 'result' is a dictionary

    return {
        "question": question,
        "result": result.get("answer"),
        "status_code": result.get("status_code")
    }
