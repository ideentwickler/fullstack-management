import re

from datetime import datetime

from app.db.session import SessionLocal
from app import models, crud, schemas

db = SessionLocal()

STATUS_LIST = [status.value.lower() for status in models.TicketStatus]


class TicketParser:
    def __init__(self, row, stores, users):
        self.row = row.lower()
        self.required_data = ['ticket_id', 'kv_nr', 'customer_name', 'store']
        self.nice_to_have_data = ['manager']
        self.stores = stores
        self.stores_names = self.stores[0]
        self.stores_internal_ids = self.stores[1]
        self.users = users

    def get_ticket_id(self) -> int:
        ticket_id = re.search(r'#\d{5}', self.row)
        ticket_id = int(ticket_id.group().replace('#', '')) if ticket_id is not None else 0
        if ticket_id != 0:
            self.required_data.remove('ticket_id')
        return ticket_id

    def get_kv_nr(self) -> int:
        kv_nr = re.search(r'\d{7}', self.row)
        kv_nr = int(kv_nr.group()) if kv_nr is not None else 0
        if kv_nr != 0:
            self.required_data.remove('kv_nr')
        return kv_nr

    def get_customer_name(self) -> str:
        customer_string = ''
        try:
            start = re.search(r'\d{7}', self.row)
            end = re.search(r' vk', self.row)
            if start and end:
                customer_string = self.row[start.end():end.start()].strip()
                remove_first_line = customer_string.index("-")
                if remove_first_line == 0:
                    customer_string = customer_string[1:len(customer_string)].strip()
                elif remove_first_line == len(customer_string)-1:
                    customer_string = customer_string[0:len(customer_string)-1].strip()
                self.required_data.remove('customer_name')
        except ValueError as e:
            customer_string = ''
        return customer_string

    def get_store(self):
        """ ZWEI WEGE - STORE DURCH NAMEN ERKENNEN ODER INNERHALB DER KLAMMERN (NLN)"""
        nln = re.search(r'\(\d{1,3}\)', self.row)
        if nln:
            nln_int = self.row[nln.start()+1:nln.end()-1] # +1 -1 entfernt: ()
            return nln_int
        else:
            store_name = [store for store in self.stores_names if (store in self.row)]
            if store_name:
                store_name = ''.join(store_name)
                return store_name

    def get_status(self):
        status = [status for status in STATUS_LIST if (status in self.row)]
        if status:
            #print("status", status)
            result = ''.join(status)
            result = result.upper()
            return models.TicketStatus(result).name
        return models.TicketStatus.NEW.name

    def get_owner(self):
        try:
            user_full_name_in_row = [name for name in self.users if (name in self.row)]
            user_join_in = ''.join(user_full_name_in_row) if user_full_name_in_row else ''
            last_name, first_name = user_join_in.split(",")
            return last_name.strip(), first_name.strip()
        except ValueError:
            return None, None

    @staticmethod
    def parse_letters(input):
        return ''.join(filter(str.isalpha, input))

    def get_kind(self) -> models.TicketKind:
        insert_ticket_kind = models.TicketKind.INCOMPLETE
        if "nachfolgeticket" in self.row and "rekla" in self.row:
            insert_ticket_kind = models.TicketKind.CLAIM
        if "nachfolgeticket" in self.row and "rekla" not in self.row:
            insert_ticket_kind = models.TicketKind.CLAIM
        if "nachfolgeticket" not in self.row and "rekla" not in self.row:
            insert_ticket_kind = models.TicketKind.COMMISSION
        if "rekla" in self.row and "nachfolgeticket" not in self.row:
            insert_ticket_kind = models.TicketKind.CLAIM
        return insert_ticket_kind.name

    def get_created_date(self):
        pat = r'\d{2}[-/.]\d{2}[-/.]\d{4}'
        check_multiple_dates = list(re.finditer(pat, self.row) or [])
        created_date = ''
        if len(check_multiple_dates) <= 2:
            created_at = re.search(pat, self.row)
            created_date = self.row[created_at.start():created_at.end()] if created_at else ''
        elif len(check_multiple_dates) == 3:
            created_date = self.row[check_multiple_dates[1].start():check_multiple_dates[1].end()]

        try:
            d, m, y = created_date.split(".")
            create_datetime = datetime.now().replace(year=int(y), month=int(m), day=int(d))
        except ValueError as e:
            create_datetime = datetime.now().replace(year=1999)
        return create_datetime

    def get_updated_date(self):
        updated_at = re.search(r'\d{2}[-/.]\d{2}[-/.]\d{4} \d{2}:\d{2}', self.row)
        updated_date = self.row[updated_at.start():updated_at.end()] if updated_at else ''

        try:
            _date, _time = updated_date.split()
            d, m, y = _date.split(".")
            h, mi = _time.split(":")
            create_datetime = datetime.now().replace(year=int(y), month=int(m), day=int(d), hour=int(h), minute=int(mi))
        except ValueError as e:
            create_datetime = datetime.now().replace(year=1999)
        return create_datetime
