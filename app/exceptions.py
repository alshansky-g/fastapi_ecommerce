"""
В модуле исключения, которые возбуждаются при crud операциях.
"""
from fastapi import HTTPException, status

CategoryNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail="Category not found")

ProductCategoryNotFound = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Category not found")

ParentCategoryNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Parent category not found")

ProductNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Product not found")

CategorySelfParentError = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail="Category cannot be its own parent")
UserExistsError = HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already registered")