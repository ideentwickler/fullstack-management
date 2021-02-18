import typing as t
from fastapi import APIRouter, Response, Request
from fastapi.responses import PlainTextResponse

from app.db.session import SessionLocal
from app.views import deps
from app.core.config import settings
from app import services, models, crud

router = APIRouter()
db = SessionLocal()


@router.get("/reporting")
def read_file(token: t.Optional[str] = None):
    if not token:
        return PlainTextResponse("Forbidden 404")

    _get_user_by_token = deps.get_current_user_by_query_token(
        token=token)  # authentication user dependency

    file = open(str(settings.SERVER_BASE_DIR) + '/test.pdf', "rb")
    file = file.read()
    print(file)
    return Response(content=file)


@router.get("/reporting")
def get_pdf(request: Request, token: str, monthrange: str) -> Response:
    """
    VIEW PATH /views/reporting
    :param monthrange:
    :param request: REQUEST INFORMATION by starlette.
    :param token: str: GET USER TOKEN
    :return:
    """
    _get_user_by_token = deps.get_current_user_by_query_token(
        token=token)  # authentication user dependency
    get_monthrange = monthrange.split(",")
    get_year = int(get_monthrange[0].split("-")[0])
    get_start_month = int(get_monthrange[0].split("-")[1])
    get_end_month = int(get_monthrange[1].split("-")[1])
    print(get_year, get_start_month, get_end_month)

    controlling_data = services.ControllingData(year=get_year, monthrange=[get_start_month, get_end_month])
    controlling_context = controlling_data.get_context().dict()
    controlling_context['headline'] = 'Gesamtübersicht'

    pdf = services.PDFGenerator(save_as='ksc-attachment.pdf', view='inline')
    pdf.new_document(template="pdf/reporting/stores.html", **controlling_context)

    for store in crud.store.get_by_kwargs(db, support=models.StoreSupport.FULL):
        store_controlling_data = services.ControllingData(
            year=get_year, monthrange=[get_start_month, get_end_month],
            store_internal_id=store.internal_id
        )
        store_controlling_context = store_controlling_data.get_context().dict()
        store_controlling_context['headline'] = store.name.upper()
        pdf.new_document(
            template='pdf/reporting/stores.html', **store_controlling_context
        )

    pdf.save_as()

    return Response(content=pdf.get_response(), media_type='application/pdf',
                    headers=pdf.get_header())
