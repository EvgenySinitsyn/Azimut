import datetime
import xlrd
from reports.models import Counterparty, Upd, Service, Payment, Object
from decimal import Decimal

PADE_INDEX_SERVICES = 1
PADE_INDEX_PAYMENTS = 0


# def set_is_relevant_false(month, year):
#     Service.objects.filter(upd__date__year=year, upd__date__month=month).update(is_relevant=False)
#     Payment.objects.filter(date__year=year, date__month=month).update(is_relevant=False)

def preparation_for_recording(work_book):
    current_period = work_book.sheet_by_index(PADE_INDEX_PAYMENTS).row_values(0)[3]
    current_period = datetime.datetime.strptime(current_period, '%d.%m.%Y').date()

    Payment.objects.filter(date__year=current_period.year, date__month=current_period.month).delete()
    Service.objects.filter(upd__date__year=current_period.year, upd__date__month=current_period.month).delete()


def parse_services(work_book, page_index):
    show_rows = work_book.sheet_by_index(page_index)
    services = []
    for i in range(1, show_rows.nrows):
        res = show_rows.row_values(i)
        counterparty_name = res[3]
        counterparty_inn = res[4]
        upd_date = res[1]
        upd_number = res[2]
        service_name = res[5]
        service_price = res[6]
        payment_object = res[0]

        if isinstance(payment_object, float):
            payment_object = str(payment_object).split('.')[0]

        object_db = Object.objects.get(name=payment_object)

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
        services.append(Service(name=service_name,
                                price=Decimal(service_price),
                                upd=upd,
                                object=object_db
                                ))

    Service.objects.bulk_create(services)


def parse_payments(work_book, page_index):
    show_rows = work_book.sheet_by_index(page_index)
    payments = []
    for i in range(show_rows.nrows):
        res = show_rows.row_values(i)
        counterparty_name = res[2]
        counterparty_inn = res[1]
        payment_date = str(res[3])
        payment_amount = res[4]
        payment_object = res[0]

        if isinstance(payment_object, float):
            payment_object = str(payment_object).split('.')[0]

        object_db = Object.objects.get(name=payment_object)

        Counterparty.objects.bulk_create([
            Counterparty(name=counterparty_name, inn=int(counterparty_inn)),
        ],
            ignore_conflicts=True)

        counterparty = Counterparty.objects.get(inn=int(counterparty_inn))

        payments.append(Payment(date=datetime.datetime.strptime(payment_date, '%d.%m.%Y').date(),
                                amount=Decimal(payment_amount),
                                counterparty=counterparty,
                                object=object_db
                                ))


    Payment.objects.bulk_create(payments)

def start_parsing(path_excel: str):
    # Counterparty.objects.all().delete()
    # Upd.objects.all().delete()
    # Service.objects.all().delete()
    # Payment.objects.all().delete()

    start_time = datetime.datetime.now()
    work_book = xlrd.open_workbook(r'{}'.format(path_excel))
    preparation_for_recording(work_book)
    parse_services(work_book, PADE_INDEX_SERVICES)
    parse_payments(work_book, PADE_INDEX_PAYMENTS)
    end_time = datetime.datetime.now()
    print((end_time - start_time))
