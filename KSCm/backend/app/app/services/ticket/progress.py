import csv
import typing as t

from app.db.session import SessionLocal
from app.core.config import settings
from app.services import TicketParser

from app import crud, models, schemas

db = SessionLocal()
file = str(settings.SERVER_BASE_DIR) + '/liste.csv'


def get_stores(_db: SessionLocal = db):
    stores = crud.store.get_multi(_db, skip=0, limit=999)
    return [store.name.lower() for store in stores], [store.internal_id for store in stores]


def ticket_exist(
        ticket_id: int,
        _db: SessionLocal = db
) -> bool:
    ticket = crud.ticket.get_by_kwargs(_db, ticket_id=ticket_id).first()
    return ticket


def get_store(_db: SessionLocal = db, *, store: t.Union[int, str]) -> int:
    if store:
        if store.isdigit():
            internal_id = int(store)
            q = crud.store.get_by_kwargs(_db, internal_id=internal_id).first()
        else:
            store_name = str(store).upper()
            q = crud.store.get_by_kwargs(_db, name=store_name).first()
        if q is not None:
            return q.internal_id

    q = crud.store.get_by_kwargs(_db, internal_id=300).first()
    return q.internal_id


def get_owner(_db: SessionLocal = db, *, user):
    if isinstance(user, tuple):
        last_name, first_name = user
        if last_name is not None and first_name is not None:
            user = crud.user.get_query(_db).filter(models.User.last_name.ilike(last_name)).first()
            return user.id
    return crud.user.get(_db, id=1).id


STORES = get_stores()
USER_LIST = [user.last_name.lower() + ', ' + user.first_name.lower() for user in crud.user.get_multi(db)]


def read_ticket_file(*, stores=STORES, users=USER_LIST, file=file):
    print(users)
    with open(file, encoding="ISO-8859-1") as csv_file:
        reader = csv.reader(csv_file, delimiter="\n")
        save_dict = {}
        x = 0
        for row in reader:
            for data in row:
                parsr = TicketParser(row=data, stores=stores, users=users)
                if "exportiert durch" in data.lower():
                    #  print("bugfix!")
                    owner = get_owner(user=parsr.get_owner())
                    if isinstance(owner, tuple):
                        owner = int(owner[0])
                    save_dict[x-1].update({
                        'owner': owner,
                        'status': parsr.get_status(),
                        'created_at': parsr.get_created_date(),
                        'updated_at': parsr.get_updated_date(),
                    })
                else:
                    add_dict = {
                        x: {
                            "kv_nr": parsr.get_kv_nr(),
                            "store": get_store(store=parsr.get_store()),
                            "ticket_id": parsr.get_ticket_id(),
                            "kind": parsr.get_kind(),
                            "status": parsr.get_status(),
                            "owner": get_owner(user=parsr.get_owner()),
                            "customer": parsr.get_customer_name(),
                            "created_at": parsr.get_created_date(),
                            "updated_at": parsr.get_updated_date(),
                        }
                    }
                    save_dict = {**save_dict, **add_dict}
                    x += 1
    csv_file.close()
    return save_dict