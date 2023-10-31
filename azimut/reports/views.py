from django.http import HttpResponse

from reports.parser import start_parsing


def index(request):
    start_parsing('reports/09Сентябрь_2023новдоговорИНН_версия181023.xls')
    return HttpResponse("Страница приложения reports", )
