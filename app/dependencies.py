from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db_depends import get_db

DBSession = Annotated[Session, Depends(get_db)]
