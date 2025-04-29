import requests
import time
from PIL import Image
import pytesseract
from io import BytesIO
from fastapi import HTTPException
from bs4 import BeautifulSoup
from app.logger import app_logger

# URLs
BASE_URL = "https://services.ecourts.gov.in/ecourtindia_v6/?p=cnr_status/searchByCNR/"
HOME_URL = "https://services.ecourts.gov.in/ecourtindia_v6/"

# Headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://services.ecourts.gov.in/ecourtindia_v6/',
    'Origin': 'https://services.ecourts.gov.in',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

def get_captcha_data(session):
    response = session.get(HOME_URL, headers=HEADERS)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to load homepage")

    time.sleep(1)

    soup = BeautifulSoup(response.text, "html.parser")
    img_tag = soup.find("img", {"id": "captcha_image"})

    if not img_tag or not img_tag.get("src"):
        raise HTTPException(status_code=500, detail="Captcha image not found on homepage")

    captcha_img_url = "https://services.ecourts.gov.in" + img_tag['src']

    app_token_input = soup.find("input", {"id": "app_token"})

    if app_token_input and app_token_input.get("value"):
        app_token = app_token_input["value"]
    else:
        app_token = ""

    return captcha_img_url, app_token

def solve_captcha(session, captcha_img_url):
    captcha_response = session.get(captcha_img_url, headers=HEADERS)

    if captcha_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to download captcha image")

    captcha_image = Image.open(BytesIO(captcha_response.content))
    captcha_text = pytesseract.image_to_string(captcha_image).strip()

    return captcha_text

def submit_form(session, cino, fcaptcha_code, app_token):
    data = {
        'cino': cino,
        'fcaptcha_code': fcaptcha_code,
        'ajax_req': 'true',
        'App_token': app_token,
    }
    response = session.post(BASE_URL, headers=HEADERS, data=data)
    return response

def process_cino_form(cino):
    session = requests.Session()

    try:
        captcha_img_url, app_token = get_captcha_data(session)
        captcha_code = solve_captcha(session, captcha_img_url)
        response = submit_form(session, cino, captcha_code, app_token)

        if response.status_code == 200:
            return {"status": "Form submitted successfully", "response": response.text}
        else:
            raise HTTPException(status_code=response.status_code, detail="Error submitting the form")

    except HTTPException as e:
        raise e
    except Exception as e:
        app_logger.error("Unhandled exception: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))
