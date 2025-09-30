from typing import Annotated

from fastapi import Depends

from app.auth import get_current_user
from app.exceptions import AuthorizationError
from app.models.users import User


class PermissionChecker:
    def __init__(self, required_roles: set):
        self.required_roles = required_roles

    def __call__(self, current_user: Annotated[User, Depends(get_current_user)]):
        if current_user.role not in self.required_roles:
            raise AuthorizationError
        return current_user


Seller = Annotated[User, Depends(PermissionChecker({"seller"}))]
Buyer = Annotated[User, Depends(PermissionChecker({"buyer"}))]
Admin = Annotated[User, Depends(PermissionChecker({"admin"}))]
