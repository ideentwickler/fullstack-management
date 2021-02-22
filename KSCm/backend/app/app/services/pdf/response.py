import typing as t
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from jinja2 import Environment, PackageLoader, select_autoescape

from app.core.config import settings

#  https://jinja.palletsprojects.com/en/2.11.x/api/#basics
jinja_env = Environment(
    loader=PackageLoader('app', 'views/templates/'),
    autoescape=select_autoescape()
)


class PDFGenerator:
    """ YOU CAN EASY GENERATE A PDF FILE WITH SEPERATED PAGES
    SIMPLY BY ADDING A NEW_DOCUMENT
    view: str = "inline" || "attachment"
    """
    def __init__(self, save_as: t.Optional[str] = 'ksc-letter.pdf', view: str = 'inline'):
        self.documents = []
        self.font_configuration = FontConfiguration()
        #  https://fastapi.tiangolo.com/advanced/response-headers/
        self.header = {
            'Content-Disposition': f'{view};filename={save_as}'
        }

    def new_document(self, *, template: str, to_documents: bool = True, **kwargs) -> None:
        template = jinja_env.get_template(template)
        template_render = template.render(**kwargs) \
            if kwargs else template.render()
        template_html = HTML(string=template_render).render(font_config=self.font_configuration)
        if template_html and to_documents:
            self.documents.append(template_html)

    def create_documents(self):
        documents = [page for document in self.documents for page in document.pages]
        create = self.documents[0].copy(documents)
        return create

    def get_header(self):
        return self.header

    def save_as(self, filename: t.Optional[str] = None) -> str:
        if not filename:
            from app.tests.utils.utils import random_lower_string
            filename = random_lower_string()

        self.create_documents().write_pdf(
            f'{str(settings.SERVER_BASE_DIR)}/'
            f'{str(settings.SERVER_MEDIA_DIR)}/{filename}.pdf'
        )
        return filename

    def get_response(self):
        self.create_documents()
        return self.create_documents().write_pdf()

