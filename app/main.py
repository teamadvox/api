from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.scraper import process_cino_form
from app.logger import app_logger

# Create FastAPI instance
app = FastAPI()

@app.get("/")
def home():
    app_logger.info("Root Executed...")
    return {"message":"Backend Running"}

# Request body model
class CinoRequest(BaseModel):
    cino: str

# Route for handling the form submission
@app.post("/submit-form")
async def submit_form(cino_request: CinoRequest):
    try:
        app_logger.info("Calling Cino Request...")
        result = process_cino_form(cino_request.cino)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
