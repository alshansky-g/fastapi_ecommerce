from fastapi import APIRouter

router = APIRouter(
    prefix="/products", tags=["products"]
)


@router.get("/")
async def get_all_products():
    """Возвращает список всех товаров."""
    return {"message": "заглушка"}


@router.post("/")
async def create_product():
    """Создаёт новый товар."""
    return {"message": "заглушка"}


@router.get("/category/{category_id}")
async def get_products_by_category(category_id: int):
    """Возвращает список товаров в указанной категории."""
    return {"message": "заглушка"}


@router.get("/{product_id}")
async def get_product(product_id: int):
    """Возвращает детальную информацию о товаре по его ID"""
    return {"message": f"Детали товара {product_id}."}


@router.put("/{product_id}")
async def update_product(product_id: int):
    """Обновляет товар по его ID"""
    return {"message": f"Товар {product_id} обновлен."}


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    """Удаляет товар по его ID"""
    return {"message": f"Товар {product_id} удален."}
