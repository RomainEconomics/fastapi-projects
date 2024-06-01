import random
import uvicorn
from fastapi import FastAPI, HTTPException, Request

from structlog import get_logger

from settings import Settings
from logger import configure_logging
from middlewares.request_logging.middleware import add_log_context
from debugger import initialize_debugger

logger = get_logger()

settings = Settings()


def init_app():
    app = FastAPI(title=settings.title)

    configure_logging(settings)

    if settings.remote_debugger:
        initialize_debugger()

    app.middleware("http")(add_log_context)

    @app.get("/log/")
    def log(request: Request):
        value = random.random()
        data = {
            "ip_address": request.client.host,
            "method": request.method,
            "value": value,
        }
        if value > 0.5:
            data |= {"status_code": 200}
            logger.info("lucky me", extra=data)
        else:
            data |= {"status_code": 400}
            logger.error("Bad luck", extra=data)
            raise HTTPException(status_code=400, detail="Bad luck")
        return {"alive": "yes"}

    @app.get("/health/")
    def health():
        return {"status": "ok"}

    @app.get("/error/")
    def error():
        raise HTTPException(status_code=400, detail="Bad luck")

    @app.get("/random/")
    def random_number():
        return {"value": random.random()}

    return app


if __name__ == "__main__":
    app = init_app()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
