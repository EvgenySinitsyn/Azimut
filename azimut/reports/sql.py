from datetime import datetime, date

from django.db import connection
from dateutil.relativedelta import relativedelta


def get_result_sheet(user_id, date_start, date_end, inn, name):
    current_date = (datetime.now() - relativedelta(months=1)).strftime('%Y-%m')
    default_start_date = current_date
    default_end_date = current_date
    condition = f" and '{current_date}-01' <= ***"

    if date_end:
        res_date_end = datetime.strptime(date_end + '-01', '%Y-%m-%d') + relativedelta(months=1)

    if date_start and date_end:
        condition = f" and '{date_start}-01' <= *** and *** < '{res_date_end}'"
        default_start_date = date_start
        default_end_date = date_end

    elif date_start:
        condition = f" and '{date_start}-01' <= ***"
        default_start_date = date_start
        default_end_date = current_date

    elif date_end:
        condition = f" and '{(res_date_end - relativedelta(months=1)).year}-01-01' <= *** and *** < '{res_date_end}'"
        default_start_date = str(date((res_date_end - relativedelta(months=1)).year, 1, 1))[:-3]
        default_end_date = date_end


    if inn:
        condition += f" and rc.inn = '{inn}'"

    if name:
        condition += f" and rc.name LIKE '%{name}%'"

    with connection.cursor() as cursor:
        cursor.execute("SET lc_time_names = 'ru_UA';")
        cursor.execute(f'''
        (SELECT rc.inn as ИНН,
		rc.name as Наименование,
		concat('УПД № ', ru.number) as Документ,
		DATE_FORMAT(ru.date, '%d.%m.%Y') as Дата_услуги,
		rs.name Наименование_услуги, 
		rs.price as Стоимость_услуг_с_налогом_всего,
		'' as Дата_платежа,
		'' as Сумма,
		'' as Месяц,
		'' as Выплата,
		ru.date as Дата
FROM reports_upd ru
    INNER JOIN reports_service rs ON ru.id = rs.upd_id
    INNER JOIN reports_counterparty rc ON ru.counterparty_id = rc.id
    INNER JOIN reports_objectgroup ro on rs.object_id = ro.object_id
    INNER JOIN auth_user_groups aug on ro.group_id = aug.group_id
where aug.user_id = {user_id} {condition.replace('***', 'ru.date')})
 
union all

(SELECT rc.inn as ИНН, 
		rc.name as Наименование,
		'' as Документ,
		'' as Дата_услуги,
		'' as Наименование_услуги, 
		'' as Стоимость_услуг_с_налогом_всего,
		DATE_FORMAT(rp.date, '%d.%m.%Y') as Дата_платежа,
		rp.amount as Сумма, 
		MONTHNAME(rp.date) as Месяц, 
		round(ro.fee / 100 * rp.amount, 2) as Выплата,
		rp.date as Дата
		
FROM reports_payment rp
    INNER JOIN reports_counterparty rc ON rp.counterparty_id = rc.id
    INNER JOIN reports_objectgroup ro on rp.object_id = ro.object_id
    INNER JOIN auth_user_groups aug on ro.group_id = aug.group_id  
   
where aug.user_id = {user_id} {condition.replace('***', 'rp.date')})
    
order by year(Дата), month(Дата), Наименование, Дата;''')

        rows = cursor.fetchall()
        return rows, default_start_date, default_end_date
