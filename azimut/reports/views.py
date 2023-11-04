from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import LoginUserForm

from reports.parser import start_parsing
from reports.sql import get_result_sheet
from decimal import Decimal


def index(request):
    start_parsing('reports/09Сентябрь 2023платежи_услуги (1).xls')
    return HttpResponse("Страница для загрузки excel")


@login_required
def result(request):
    user_id = request.user.id
    date_start = None
    date_end = None
    inn = None
    name = None
    if request.method == 'POST':
        if "download_file" in request.POST:
            files = request.FILES.getlist('excel_file')
            for file in files:
                print(file)

        elif "filter" in request.POST:
            date_start = request.POST['date_start']
            date_end = request.POST['date_end']
            inn = request.POST['inn']
            name = request.POST['name']
            print(user_id, date_start, date_end, inn, name)

    result_sheet = get_result_sheet(user_id,
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
               'amount_services': amount_services,
               'amount_payments': amount_payments,
               'amount_fee': amount_fee,
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
