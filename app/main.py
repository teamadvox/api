from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.scraper import process_cino_form

# Create FastAPI instance
app = FastAPI()

# Request body model
class CinoRequest(BaseModel):
    cino: str

# Route for handling the form submission
@app.post("/submit-form")
async def submit_form(cino_request: CinoRequest):
    try:
        result = process_cino_form(cino_request.cino)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
