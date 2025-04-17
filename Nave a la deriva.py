from fastapi import FastAPI, Response, status
from fastapi.responses import HTMLResponse
import random

app = FastAPI()

SYSTEMS = ["navigation", "communications", "life_support", "engines", "deflector_shield"]

SYSTEM_CODES = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}

damaged_system = None

@app.get("/status")
async def get_status():
    global damaged_system
    
    damaged_system = random.choice(SYSTEMS)

    return {"damaged_system": damaged_system}

@app.get("/repair-bay", response_class=HTMLResponse)
async def repair_bay():
    global damaged_system
    
    repair_code = SYSTEM_CODES[damaged_system]
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair</title>
    </head>
    <body>
        <div class="anchor-point">{repair_code}</div>
    </body>
    </html>
    """
    
    return html_content

@app.post("/teapot")
async def teapot(response: Response):
    response.status_code = status.HTTP_418_IM_A_TEAPOT
    return {"message": "I'm a teapot"}