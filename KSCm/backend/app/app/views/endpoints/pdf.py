import typing as t
from fastapi import APIRouter, Response, Request
from babel.numbers import format_number
from pydantic import BaseModel
from app.db.session import SessionLocal
from app.views import deps
from app import services, models

router = APIRouter()

db = SessionLocal()


class FirstPageContext(BaseModel):
    headline: str
    months: t.List[str]
    commissions: t.List[int]
    claims: t.List[int]
    processing: t.Dict[str, int]
    bills: t.Dict[str, t.Any]


@router.get("/reporting")
def get_pdf(request: Request, token: str) -> Response:
    print(request.client)
    print(request.headers)
    _get_user_by_token: models.User = deps.get_current_user_by_query_token(
        token=token)  # noqa F841
    calendar = services.ControllingCalendar(year=2020, monthrange=[1, 12]).get()
    context = FirstPageContext(
        headline='Gesamtübersicht',
        months=[month for month in calendar.keys() if (month != 'range')],
        claims=[],
        commissions=[],
        processing={},
        bills={},
    )

    months_label_list = [month for month in calendar.keys() if (month != 'range')]
    months_commission_count = []
    months_claims_count = []

    start, end = calendar['range']['start'], calendar['range']['end']
    for process in models.TicketStatus:
        process_count = services.get_tickets_count(
            db, start=start, end=end, status=process)
        context.processing[process.name] = process_count

    context.bills.update(
        {
            'bill': services.get_claim_bill(db, start=start, end=end,
                                            calculation="sum"),
            'discharge': services.get_clean_discharge(db, start=start, end=end),
            'total': services.get_claim_bill(db, start=start, end=end,
                                             calculation="sum")
                     - services.get_clean_discharge(db, start=start, end=end)
        }
    )

    for month in months_label_list:
        start, end = calendar[month]['start'], calendar[month]['end']
        month_commission_count = services.get_tickets_count(db, start=start, end=end,
                                                            kind=models.TicketKind.COMMISSION)
        context.months.append(month_commission_count)
        months_commission_count.append(month_commission_count)
        month_claims_count = services.get_tickets_count(db, start=start, end=end,
                                                        kind=models.TicketKind.CLAIM)
        context.claims.append(month_claims_count)
        months_claims_count.append(month_claims_count)

    commissions_total = sum(months_commission_count)
    claims_total = sum(months_claims_count)
    total_total = commissions_total + claims_total

    commissions_average = commissions_total / len(months_label_list)
    commissions_average = int(round(commissions_average, 0))
    claims_average = claims_total / len(months_label_list)
    claims_average = int(round(claims_average, 0))
    total_average = total_total / len(months_label_list)
    total_average = int(round(total_average, 0))

    months_total_zip = zip(months_commission_count, months_claims_count)
    months_total_count = [x + y for (x, y) in months_total_zip]

    plot = services.CreatePlot(
        labels=months_label_list,
        values={
            'Kommissionen': months_commission_count,
            'Reklamationen': months_claims_count
        },
        colors=['blue', 'red'],
    )

    pdf = services.PDFGenerator(save_as='ksc-attachment.pdf', view='inline')
    #  http://babel.pocoo.org/en/latest/numbers.html
    format_claims = format_number(
        round(services.get_claim_bill(db, calculation='sum'), 0), locale='de_DE')
    format_discharge = format_number(round(services.get_clean_discharge(db), 0),
                                     locale='de_DE', )
    site_kwargs = {
        'months': months_label_list,
        'commissions': months_commission_count,
        'claims': months_claims_count,
        'commissions_total': commissions_total,
        'claims_total': claims_total,
        'total_total': total_total,
        'commissions_average': commissions_average,
        'claims_average': claims_average,
        'total_average': total_average,
        'plot': plot.get_data(),
        'testdict': {'one': 'eins', 'two': 'zwo'},
        'py': context,
        'total': months_total_count,
        '_total': services.get_tickets_count(db),
        'claims_bill': format_claims,
        'bla': format_discharge,
    }
    pdf.new_document(template="pdf/reporting/stores.html",
                     **site_kwargs)  # **context.dict()
    pdf.new_document(template="pdf/reporting/stores.html", **site_kwargs)

    return Response(content=pdf.get_response(), media_type='application/pdf',
                    headers=pdf.get_header())
