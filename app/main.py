from fastapi import FastAPI

from app.log import LogMiddleware
from app.routers import categories, products, reviews, users
from app.tasks import call_background_task

app = FastAPI(
    title="FastAPI интернет-магазин", version="0.1.0"
)
app.add_middleware(LogMiddleware)

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(reviews.router)


@app.get("/")
async def root(message: str, delay: int | float = 5):
    """Корневой маршрут, подтверждающий, что API работает."""
    call_background_task.delay(message, delay)
    return {"message": "API интернет магазина"}
