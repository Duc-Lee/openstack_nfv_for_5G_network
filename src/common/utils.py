from fastapi import FastAPI
import logging

def create_app(title: str) -> FastAPI:
    app = FastAPI(title=title)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    @app.get("/health")
    async def health():
        return {"status": "healthy", "service": title.split()[1] if len(title.split()) > 1 else title}
    return app
