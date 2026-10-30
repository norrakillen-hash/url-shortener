from fastapi import FastAPI

app = FastAPI(title="URL Shortener")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"service": "url-shortener", "version": "0.1.0"}
