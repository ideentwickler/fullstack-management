from fastapi import APIRouter, Response, Request

from app.db.session import SessionLocal
from app.views import deps
from app import services, models, crud

router = APIRouter()
db = SessionLocal()


@router.get("/reporting")
def get_pdf(request: Request, token: str) -> Response:
    """
    VIEW PATH /views/reporting
    :param request: REQUEST INFORMATION by starlette.
    :param token: str: GET USER TOKEN
    :return:
    """
    _get_user_by_token = deps.get_current_user_by_query_token(
        token=token)  # authentication user dependency
    controlling_data = services.ControllingData(year=2020)
    controlling_context = controlling_data.get_context().dict()
    controlling_context['headline'] = 'Gesamtübersicht'

    pdf = services.PDFGenerator(save_as='ksc-attachment.pdf', view='inline')
    pdf.new_document(template="pdf/reporting/stores.html", **controlling_context)

    for store in crud.store.get_by_kwargs(db, support=models.StoreSupport.FULL):
        store_controlling_data = services.ControllingData(
            year=2020, store_internal_id=store.internal_id
        )
        store_controlling_context = store_controlling_data.get_context().dict()
        store_controlling_context['headline'] = store.name.upper()
        pdf.new_document(
            template='pdf/reporting/stores.html', **store_controlling_context
        )

    return Response(content=pdf.get_response(), media_type='application/pdf',
                    headers=pdf.get_header())
