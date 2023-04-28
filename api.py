from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["root"])
async def read_root():
    print("game connected trhough api")
    return {"message": "documents api @bhunao"}
