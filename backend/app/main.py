from fastapi import FastAPI

app = FastAPI(title="API Principal")

@app.get("/")
def read_root():
    return {"message": "Backend operante!"}