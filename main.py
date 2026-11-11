from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def start():
    return { "message" : "BookingCRM Api is running"}