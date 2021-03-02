import time

from celery import current_task
from datetime import datetime

from app.db.session import SessionLocal
from app.core.celery_app import celery_app
from app.services.ticket import progress
from app.services.controlling import ControllingCalendar
from app.services.claim.sys import iter_claim_rows, get_file
from app import crud, models, schemas, services

db = SessionLocal()


@celery_app.task(acks_late=True)
def progress_claim_data(filepath):

    rows = iter_claim_rows(file=get_file(filepath))
    for row in rows:
        ticket_exist = crud.ticket.get_by_kwargs(
            db, contract_nr=row.contract_nr, kind=models.TicketKind.COMMISSION).first()
        if ticket_exist:
            # UPDATE CLAIM DATA
            # TODO: check it out!
            row.store_internal_id = ticket_exist.store_internal_id
            row.owner_id = ticket_exist.owner_id
            row.ticket_id = ticket_exist.ticket_id

            print("...ticket ->", ticket_exist.ticket_id)
            claim_exist = crud.claim.get_by_kwargs(db, contract_nr=row.contract_nr,
                                                   created_at=row.created_at,
                                                   bill=row.bill).first()
            if not claim_exist:
                print("...claim not exist!")
                claim = crud.claim.create(db, obj_in=row)
                if claim:
                    print(f"...created new claim {claim.id}")
            else:
                print("...claim exist!")
                claim = crud.claim.update(db, db_obj=claim_exist, obj_in=row)
                if claim:
                    print(f"...updated claim {claim.id}")

    return 'success'


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


public_static_data = {}


@celery_app.task
def progress_static_data():
    print("started...")
    static_data = {}
    try:
        years = crud.ticket.get_date_parts(db, column="created_at", part="YEAR")
        years = [year for year in years if (year != 1999)]
        supported_stores = crud.store.get_supported(db)
        for year in years:
            static_data[year] = {}
            # STORE DATA PER YEAR
            for store in supported_stores:
                store_controlling_data = services.ControllingData(year=year, store_internal_id=store.internal_id, create_plot=False).get_context().dict()
                static_data[year].update({
                    store.name: store_controlling_data
                })
            # TOTAL DATA PER YEAR
            year_controlling_data = services.ControllingData(year=year, create_plot=False).get_context().dict()
            static_data[year].update({
                'TOTAL': year_controlling_data,
            })
    except ValueError:
        print("error...")
    finally:
        print("static data refreshed...")
        public_static_data.update(static_data)
    return 'finished'



TEST_LIST = []

@celery_app.task
def checker():
    x = 10
    TEST_LIST.append(x)
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
def progress_ticket_data(filepath):
    i = 0
    tickets = progress.read_ticket_file(file=filepath)
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



