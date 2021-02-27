import time
from celery import current_task
from datetime import datetime
from app.db.session import SessionLocal
from app.core.celery_app import celery_app
from app.services.ticket import progress
from app.services.controlling import ControllingCalendar
from app import crud, models, schemas

db = SessionLocal()


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task(acks_late=True)
def test_test():
    s = 0
    while s != 30:
        time.sleep(1)
        print(s)
        s += 1
    return 'finished'


@celery_app.task
def checker():
    print("Hello 10 Seconds!")


def get_active_stores(_db=db, exclude_store_internal_id: list=[300], *, start: datetime, end: datetime):
    stores_list = []
    stores = crud.store.get_query(_db).all()
    for store in stores:
        more_than_zero = crud.ticket.get_query(db).filter(models.Ticket.created_at.between(start, end)).filter(
            models.Ticket.store_internal_id == store.internal_id).count()
        if more_than_zero:
            if store.id not in exclude_store_internal_id:
                stores_list.append(store.name)
    return stores_list


def get_static_data(db):
    calendar = ControllingCalendar(year=2020, monthrange=[1, 12]).get()
    labels = [month for month in calendar]
    total = []
    kinds = [kind.name for kind in models.TicketKind]
    per_kind = []
    status = [status.name for status in models.TicketStatus]
    per_status = []

    start = calendar['range']['start']
    end = calendar['range']['end']

    stores_list = get_active_stores(_db=db, start=start, end=end)

    for month in calendar.values():
        result = crud.ticket.get_query(db).filter(models.Ticket.created_at.between(month['start'], month['end'])).count()
        total.append(result)
        for kind in kinds:
            result = crud.ticket.get_query(db).filter(models.Ticket.created_at.between(month['start'], month['end'])).filter(models.Ticket.kind == kind).count()
            per_kind.append(result)
        for sta in status:
            result = crud.ticket.get_query(db).filter(
                models.Ticket.created_at.between(month['start'], month['end'])).filter(
                models.Ticket.status == sta).count()
            per_status.append(result)

    return {
        'stores': stores_list,
        'labels': labels,
        'total': total,
        'kinds': kinds,
        'per_kind': per_kind,
        'status': status,
        'per_status': per_status,
    }


@celery_app.task(acks_late=True)
def progress_ticket_data():
    i = 0
    tickets = progress.read_ticket_file()
    tickets_len = len(tickets)
    for key, val in tickets.items():
        if val['kv_nr'] != 0 and val['ticket_id'] != 0:
            i += 1
            if i % 100 == 1:
                print("sleeping a second...")
                time.sleep(1)
            current_task.update_state(state='PROGRESS', meta={'process': f'{i}/{tickets_len}'})
            check_ticket = progress.ticket_exist(ticket_id=val['ticket_id'])
            if not check_ticket:
                ticket_in = schemas.TicketCreate(
                    ticket_id=val['ticket_id'],
                    contract_nr=val['kv_nr'],
                    customer_name=val['customer'],
                    status=val['status'],
                    kind=val['kind'],
                    owner_id=val['owner'],
                    store_internal_id=val['store'],
                    created_at=val['created_at'],
                    updated_at=val['updated_at'],
                )
                ticket = crud.ticket.create(db, obj_in=ticket_in)
                if ticket:
                    print(f"...created new ticket #{ticket.ticket_id}")
            else:
                db_obj = crud.ticket.get_by_kwargs(db, ticket_id=val['ticket_id']).first()
                ticket_in = schemas.TicketUpdate(
                    owner_id=val['owner'],
                    status=val['status'],
                    updated_at=val['updated_at']
                )
                ticket = crud.ticket.update(db, db_obj=db_obj, obj_in=ticket_in)
                if ticket:
                    print(f"...updated ticket #{ticket.ticket_id}")

    return 'finished'
