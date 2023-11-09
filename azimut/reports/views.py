from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import LoginUserForm

from reports.parser import start_parsing
from reports.sql import get_result_sheet
from decimal import Decimal

from .models import ObjectGroup


def index(request):
    start_parsing('reports/09Сентябрь 2023платежи_услуги (1).xls')
    return HttpResponse("Страница для загрузки excel")


@login_required
def result(request):
    user_id = request.user.id
    user_name = request.user
    date_start = None
    date_end = None
    inn = None
    name = None
    group = request.user.groups.get()
    group_name = group.name
    fee = ObjectGroup.objects.filter(group=group)[0].fee

    if request.method == 'POST':
        if "download_file" in request.POST:
            files = request.FILES.getlist('excel_file')
            file_name = str(files[0])

            with open(f'./files/{file_name}', 'wb+') as destination:
                for chunk in files[0].chunks():
                    destination.write(chunk)
            start_parsing(f'./files/{file_name}')
            # messages.info(request, 'файл загружен')

        elif "filter" in request.POST:
            date_start = request.POST['date_start']
            date_end = request.POST['date_end']
            inn = request.POST['inn']
            name = request.POST['name']

    result_sheet, \
    default_start_date, \
    default_end_date = get_result_sheet(user_id,
                                        date_start,
                                        date_end,
                                        inn,
                                        name)

    amount_services, amount_fee, amount_payments = 0, 0, 0
    for row in result_sheet:
        amount_services += Decimal(row[5] if row[5] else 0)
        amount_payments += Decimal(row[7] if row[7] else 0)
        amount_fee += Decimal(row[9] if row[9] else 0)
    context = {'result_sheet': result_sheet,
               'amount_services': '{0:,}'.format(amount_services).replace(',', ' '),
               'amount_payments': '{0:,}'.format(amount_payments).replace(',', ' '),
               'amount_fee': '{0:,}'.format(amount_fee).replace(',', ' '),
               'group_name': group_name,
               'user_name': user_name,
               'fee': fee,
               'default_start_date': default_start_date,
               'default_end_date': default_end_date,
               }

    return render(request, 'reports/result.html', context=context)


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'reports/login.html'

    def get_success_url(self):
        url = reverse_lazy('result')
        return url


def logout_user(request):
    logout(request)
    return redirect('login')


# def serverError(request, exception):
#     return HttpResponseServerError('<h1>Проверьте корректность загруженного файла</h1>')