from app.routers import categories
from fastapi import FastAPI

app = FastAPI(
    title="FastAPI интернет-магазин", version="0.1.0"
)
app.include_router(categories.router)


@app.get("/")
async def root():
    """Корневой маршрут, подтверждающий, что API работает."""
    return {"message": "API интернет магазина"}
