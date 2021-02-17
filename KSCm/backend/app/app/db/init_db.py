from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.core.config import settings
from app.db import base, init_data  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            first_name='Administrator',
            last_name='FastAPI',
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        if user:
            print(f"...created superuser {user.email}")

    for user in init_data.BASE_USER:
        if not crud.user.get_by_email(db, email=user['email']):
            user_in = schemas.UserCreate(
                email=user['email'],
                password=init_data.generate_random_password(),
                first_name=user['first_name'],
                last_name=user['last_name'],
            )
            user = crud.user.create(db, obj_in=user_in)
            if user:
                print(f"...created user {user.email}")

    for store in init_data.BASE_STORES.split("\n"):
        try:
            internal_id, name, ceo = store.split(";")
            if not crud.store.get_by_kwargs(db, internal_id=internal_id).first():
                store_in = schemas.StoreCreate(
                    internal_id=internal_id,
                    name=name.upper(),
                    support=models.store.StoreSupport.DISABLED.name,
                )
                store = crud.store.create(db, obj_in=store_in)
                if store:
                    print(f"...created store {store.internal_id} {store.name}")
        except ValueError:
            pass

    print("base_dir", settings.SERVER_BASE_DIR)