from sqlalchemy.orm import Session


class DBSessionContext(object):
    def __init__(self, db: Session) -> None:
        self.db = db


class AppService(DBSessionContext):
    pass
