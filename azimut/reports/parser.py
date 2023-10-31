import datetime
import xlrd
from reports.models import Counterparty, Upd, Service, Payment, Object
from decimal import Decimal

PADE_INDEX_SERVICES = 10
PADE_INDEX_PAYMENTS = 9


def parse_services(work_book, page_index):
    show_rows = work_book.sheet_by_index(page_index)
    for i in range(1, show_rows.nrows):
        res = show_rows.row_values(i)
        counterparty_name = res[3]
        counterparty_inn = res[4]
        upd_date = res[1]
        upd_number = res[2]
        service_name = res[5]
        service_price = res[6]

        Counterparty.objects.bulk_create([
            Counterparty(name=counterparty_name, inn=counterparty_inn),
        ],
            ignore_conflicts=True)
        counterparty = Counterparty.objects.get(inn=counterparty_inn)

        Upd.objects.bulk_create([
            Upd(date=datetime.datetime.strptime(upd_date, '%d.%m.%Y').date(),
                number=res[2],
                counterparty=counterparty)
        ],
            ignore_conflicts=True)
        upd = Upd.objects.get(number=upd_number)

        Service.objects.create(name=service_name,
                               price=Decimal(service_price),
                               upd=upd
                               )


def parse_payments(work_book, page_index):
    show_rows = work_book.sheet_by_index(page_index)
    for i in range(0, show_rows.nrows):
        res = show_rows.row_values(i)
        counterparty_name = res[2]
        counterparty_inn = res[1]
        payment_date = res[3]
        payment_amount = res[4]
        payment_object = res[0]

        if isinstance(payment_object, float):
            payment_object = str(payment_object).split('.')[0]

        object_db = Object.objects.get(name=payment_object)

        # #TODO обработать возможную ошибку

        Counterparty.objects.bulk_create([
            Counterparty(name=counterparty_name, inn=int(counterparty_inn)),
        ],
            ignore_conflicts=True)

        counterparty = Counterparty.objects.get(inn=int(counterparty_inn))

        Payment.objects.create(date=datetime.datetime.strptime(payment_date, '%d.%m.%Y').date(),
                               amount=Decimal(payment_amount),
                               counterparty=counterparty,
                               object=object_db
                               )


def start_parsing(path_excel: str):
    # Counterparty.objects.all().delete()
    # Upd.objects.all().delete()
    # Service.objects.all().delete()
    # Payment.objects.all().delete()

    work_book = xlrd.open_workbook(r'{}'.format(path_excel))
    parse_services(work_book, PADE_INDEX_SERVICES)
    parse_payments(work_book, PADE_INDEX_PAYMENTS)
