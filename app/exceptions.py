"""
Модуль с наиболее востребованными исключениями.
"""
from fastapi import HTTPException, status

# Исключения CRUD.
CategoryNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

ProductCategoryNotFound = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found"
)

ParentCategoryNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Parent category not found"
)

ProductNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Product not found or inactive")

CategorySelfParentError = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Category cannot be its own parent"
)
UserExistsError = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
)
ReviewNotFoundError = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Review not found or inactive"
)


# Исключения аутентификации.
BadCredentialsError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
ExpiredTokenError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired",
    headers={"WWW-Authenticate": "Bearer"},
)
IncorrectCredentialsError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
    headers={"WWW-Authenticate": "Bearer"},
)
RefreshTokenValidationError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate refresh token",
    headers={"WWW-Authenticate": "Bearer"},
)

# Исключения авторизации
AuthorizationError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You're not authorized to perform this action"
)
NotProductOwnerError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="You can only change your own products"
)
ReviewAlreadyExists = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You can only create one review per product"
)
