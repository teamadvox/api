from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Add this
from pydantic import BaseModel
from api.app.scraper import process_cino_form
from api.app.logger import app_logger

# Create FastAPI instance
app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow your React dev origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
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
