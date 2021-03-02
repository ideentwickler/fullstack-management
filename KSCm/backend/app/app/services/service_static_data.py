from typing import TypeVar

from app.utils.app_exceptions import AppException
from app.utils.service_result import ServiceResult
from app.services.main import AppService
from pydantic import BaseModel

from app import crud, services

RequestType = TypeVar("RequestType", bound=BaseModel)


class StaticDataService(AppService):
    """
    SERVICE object to handle all kind business logic stuff.

    """
    def get(self):
        static_data = {}
        try:
            years = crud.ticket.get_date_parts(self.db, column="created_at",
                                               part="YEAR")
            years = [year for year in years if (year != 1999)]
            supported_stores = crud.store.get_supported(self.db)
            for year in years:
                static_data[year] = {}
                # STORE DATA PER YEAR
                for store in supported_stores:
                    store_controlling_data = services. \
                        ControllingData(year=year,
                                        store_internal_id=store.internal_id,
                                        create_plot=False).get_context().dict()
                    static_data[year].update({
                        store.name: store_controlling_data
                    })
                # TOTAL DATA PER YEAR
                year_controlling_data = services. \
                    ControllingData(year=year, create_plot=False).get_context().dict()
                static_data[year].update({
                    'TOTAL': year_controlling_data,
                })
        finally:
            print("yeah")
        return ServiceResult(static_data)

