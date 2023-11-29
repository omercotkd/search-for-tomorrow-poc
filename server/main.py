from fastapi import FastAPI
import routers

app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": 0})

app.include_router(routers.router)
