import calendar
import typing as t

from datetime import datetime
from pydantic import BaseModel
from babel.numbers import format_number

from app.db.session import SessionLocal
from app import models, crud, services, schemas

db = SessionLocal()

DATE_MONTHS = (
    (0, ''),
    (1, 'Jan'),
    (2, 'Feb'),
    (3, 'Mrz'),
    (4, 'Apr'),
    (5, 'Mai'),
    (6, 'Jun'),
    (7, 'Jul'),
    (8, 'Aug'),
    (9, 'Sep'),
    (10, 'Okt'),
    (11, 'Nov'),
    (12, 'Dez'),
)


class ControllingCalendar:
    def __init__(
            self,
            *,
            year: int = None,
            monthrange: t.List = None,
            auto_until_now: bool = False,
    ) -> None:
        self.year = year \
            if year is not None else int(datetime.now().year)
        self.monthrange = monthrange \
            if monthrange is not None else [1, 12]
        self.date_time: datetime = datetime.now()
        self.data: dict = {}
        self.create()

    def get_month_days(self, *, month: int) -> calendar.monthrange:
        return calendar.monthrange(self.year, month)[1]

    def get_datetime_monthrange(self, *, month) -> t.Tuple[datetime, datetime]:
        start = self.date_time.replace(year=self.year, month=month, day=1, hour=0, minute=0)
        end = self.date_time.replace(year=self.year, month=month,
                                     day=self.get_month_days(month=month),
                                     hour=23, minute=59)
        return start, end

    @staticmethod
    def get_month_label(*, month: int) -> str:
        return DATE_MONTHS[month][1]

    def get_total_range(self):
        start = self.data[list(self.data)[0]]['start']
        end = self.data[list(self.data)[-1]]['end']
        return {
            'range': {
                'start': start,
                'end': end,
            }
        }

    def create(self) -> t.Dict:
        for i in range(self.monthrange[0], self.monthrange[1] + 1):
            iter_month = self.get_month_label(month=i)
            start, end = self.get_datetime_monthrange(month=i)
            self.data[iter_month] = {
                'start': start,
                'end': end,
            }
        self.data.update(self.get_total_range())
        return self.data

    def get(self) -> t.Dict:
        return self.data


class FirstPageContext(BaseModel):
    headline: t.Optional[str] = None
    months: t.Optional[t.List[str]] = []
    counts: t.Optional[t.Dict[str, t.List[int]]] = {}
    processing: t.Optional[t.Dict[str, t.List[int]]] = {}
    bills: t.Optional[t.Dict[str, t.Any]] = {}
    benchmarks: t.Optional[t.Dict[str, t.Any]] = {}
    plot: t.Any = None


class ControllingData(ControllingCalendar):
    def __init__(
            self, year: int = None, monthrange: t.List = None,
            store_internal_id: int = None, owner_id: int = None
    ) -> None:
        super().__init__(year=year, monthrange=monthrange)
        self.months_labels = [month for month in self.data.keys() if (month != 'range')]
        self.start = self.data['range']['start']
        self.end = self.data['range']['end']
        self.store_internal_id = store_internal_id
        self.owner_id = owner_id
        self.context: FirstPageContext = FirstPageContext()

    def get_ticket_count_per_kind_and_month(self) -> None:
        for kind in models.TicketKind:
            count_per_month = []
            for m in self.months_labels:
                ticket_count = services.get_tickets_count(
                    db,
                    start=self.data[m]['start'],
                    end=self.data[m]['end'],
                    kind=kind,
                    store_internal_id=self.store_internal_id,
                    owner_id=self.owner_id,
                )
                count_per_month.append(ticket_count)
            self.context.counts[kind.name] = count_per_month
        self.context.counts['TOTAL'] = [
            x + y for (x, y) in zip(
                self.context.counts[models.TicketKind.COMMISSION.name],
                self.context.counts[models.TicketKind.CLAIM.name])
        ]
        return

    def get_ticket_count_per_status_process(self) -> None:
        for process in models.TicketStatus:
            count_per_process = []
            for m in self.months_labels:
                ticket_count = services.get_tickets_count(
                    db,
                    start=self.data[m]['start'],
                    end=self.data[m]['end'],
                    status=process,
                    store_internal_id=self.store_internal_id,
                    owner_id=self.owner_id,
                )
                count_per_process.append(ticket_count)
            self.context.processing[process.name] = count_per_process
        return

    @staticmethod
    def get_local_format(float_sum: t.Union[float, int], round_int: int = 0) -> str:
        rounded_sum = round(float_sum, round_int)
        local_sum = format_number(rounded_sum, locale='de_DE')
        return local_sum

    def get_clean_claim_bill(self) -> float:
        claim_bill_sum = services.get_claim_bill(
            db,
            start=self.start,
            end=self.end,
            store_internal_id=self.store_internal_id,
            owner_id=self.owner_id,
            calculation="sum"
        )
        claim_discharge_sum = services.get_clean_discharge(
            db,
            start=self.start,
            end=self.end,
            store_internal_id=self.store_internal_id,
            owner_id=self.owner_id,
        )
        clean_bill = claim_discharge_sum + claim_bill_sum
        print("clean bill", clean_bill)
        return clean_bill if clean_bill else 0

    def get_claim_bill_formatted(self) -> float:
        claim_bill_sum = services.get_claim_bill(
            db,
            start=self.start,
            end=self.end,
            store_internal_id=self.store_internal_id,
            owner_id=self.owner_id,
            calculation="sum"
        )
        claim_discharge_sum = services.get_clean_discharge(
            db,
            start=self.start,
            end=self.end,
            store_internal_id=self.store_internal_id,
            owner_id=self.owner_id,
        )
        claim_bill_discharge_dif = self.get_clean_claim_bill()
        claim_count = services.get_claim_bill(
            db,
            start=self.start,
            end=self.end,
            store_internal_id=self.store_internal_id,
            owner_id=self.owner_id,
            calculation="count"
        )
        self.context.bills.update({
            'count': claim_count,
            'bill': self.get_local_format(claim_bill_sum),
            'discharge': self.get_local_format(claim_discharge_sum),
            'total': self.get_local_format(claim_bill_discharge_dif),
        })
        return claim_bill_discharge_dif

    def get_benchmarks(self) -> None:
        claim_average = services.get_claim_bill(
            db,
            start=self.start,
            end=self.end,
            store_internal_id=self.store_internal_id,
            owner_id=self.owner_id,
            calculation="avg",
        )
        claim_average_format = self.get_local_format(claim_average, 2)
        ticket_count = sum(self.context.counts[models.TicketKind.COMMISSION.name])
        print("ticket count", ticket_count)
        try:
            claim_average_per_commission = self.get_clean_claim_bill() / ticket_count
        except ZeroDivisionError:
            claim_average_per_commission = 0.00
        claim_average_per_commission_format = self.get_local_format(claim_average_per_commission, 2)
        self.context.benchmarks.update({
            'claim': claim_average_format,
            'commission': claim_average_per_commission_format,
        })
        return

    def get_plot(self) -> None:
        plot = services.CreatePlot(
            labels=self.context.months,
            values={
                'Kommissionen': self.context.counts[models.TicketKind.COMMISSION.name],
                'Reklamationen': self.context.counts[models.TicketKind.CLAIM.name],
            },
            colors=['blue', 'red'],
        )
        self.context.plot = plot.get_data()
        return

    def get_context(self):
        self.get_ticket_count_per_kind_and_month()
        self.get_ticket_count_per_status_process()
        self.get_claim_bill_formatted()
        self.context.months = self.months_labels
        self.get_plot()
        self.get_benchmarks()
        return self.context



