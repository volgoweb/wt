# -*- coding: utf-8 -*-
import datetime
from dateutil.relativedelta import relativedelta

from app.account.models import Account, CompanyUnit
from app.task.models import Task, TaskTemplate
from app.crm.models import DealStatus
from app.contact.models import Company, Contact


class DemoData():
    def __init__(self, *args, **kwargs):
        self.now = datetime.datetime.now()
        self.today = datetime.date.today()
        self.next_month = self.today + relativedelta(months=1)

    def create_demo_company_units(self):
        self.demo_company_units = {}

        self.demo_company_units['director'] = CompanyUnit(
            name=u'Директор',
            unit_type=CompanyUnit.UNIT_TYPE_EMPLOYEE,
        )
        self.demo_company_units['director'].save()

        self.demo_company_units['sales_dep'] = CompanyUnit(
            name=u'Отдел продаж',
            unit_type=CompanyUnit.UNIT_TYPE_DEPARTMENT,
            parent=self.demo_company_units['director'],
        )
        self.demo_company_units['sales_dep'].save()

        self.demo_company_units['boss_sales_dep'] = CompanyUnit(
            name=u'Начальник отдела продаж',
            unit_type=CompanyUnit.UNIT_TYPE_EMPLOYEE,
            parent=self.demo_company_units['sales_dep'],
        )
        self.demo_company_units['boss_sales_dep'].save()

        self.demo_company_units['manager_sales_dep'] = CompanyUnit(
            name=u'Менеджер отдела продаж',
            unit_type=CompanyUnit.UNIT_TYPE_EMPLOYEE,
            parent=self.demo_company_units['boss_sales_dep'],
        )
        self.demo_company_units['manager_sales_dep'].save()

        self.demo_company_units['buying_dep'] = CompanyUnit(
            name=u'Отдел закупок',
            unit_type=CompanyUnit.UNIT_TYPE_DEPARTMENT,
            parent=self.demo_company_units['director'],
        )
        self.demo_company_units['buying_dep'].save()

        self.demo_company_units['boss_buying_dep'] = CompanyUnit(
            name=u'Начальник отдела закупок',
            unit_type=CompanyUnit.UNIT_TYPE_EMPLOYEE,
            parent=self.demo_company_units['buying_dep'],
        )
        self.demo_company_units['boss_buying_dep'].save()

        self.demo_company_units['manager_buying_dep'] = CompanyUnit(
            name=u'Менеджер отдела закупок',
            unit_type=CompanyUnit.UNIT_TYPE_EMPLOYEE,
            parent=self.demo_company_units['boss_buying_dep'],
        )
        self.demo_company_units['manager_buying_dep'].save()

    def create_demo_accounts(self):
        self.demo_accounts = {}
        self.demo_accounts['admin'] = Account(
            email='admin@test.test',
            first_name=u'Дмитрий',
            last_name=u'Иванцев',
            is_superuser=True,
        )
        self.demo_accounts['admin'].save()
        self.demo_accounts['admin'].set_password('admin')
        self.demo_accounts['admin'].save()

        self.demo_accounts['director'] = Account(
            email='director@test.test',
            first_name=u'Константин',
            last_name=u'Маслов',
            job=self.demo_company_units['director'],
        )
        self.demo_accounts['director'].save()
        self.demo_accounts['director'].set_password('director')
        self.demo_accounts['director'].save()

        self.demo_accounts['boss_sales_dep'] = Account(
            email='boss_sales_dep@test.test',
            first_name=u'Василий',
            last_name=u'Перов',
            department=self.demo_company_units['sales_dep'],
            job=self.demo_company_units['boss_sales_dep'],
        )
        self.demo_accounts['boss_sales_dep'].save()
        self.demo_accounts['boss_sales_dep'].set_password('boss_sales_dep')
        self.demo_accounts['boss_sales_dep'].save()

        self.demo_accounts['manager_sales_dep'] = Account(
            email='manager_sales_dep@test.test',
            password='manager_sales_dep',
            first_name=u'Петр',
            last_name=u'Латоев',
            department=self.demo_company_units['sales_dep'],
            job=self.demo_company_units['manager_sales_dep'],
        )
        self.demo_accounts['manager_sales_dep'].save()
        self.demo_accounts['manager_sales_dep'].set_password('manager_sales_dep')
        self.demo_accounts['manager_sales_dep'].save()

        self.demo_accounts['boss_buying_dep'] = Account(
            email='boss_buying_dep@test.test',
            password='boss_buying_dep',
            first_name=u'Тимофей',
            last_name=u'Портнов',
            department=self.demo_company_units['buying_dep'],
            job=self.demo_company_units['boss_buying_dep'],
        )
        self.demo_accounts['boss_buying_dep'].save()
        self.demo_accounts['boss_buying_dep'].set_password('boss_buying_dep')
        self.demo_accounts['boss_buying_dep'].save()

        self.demo_accounts['manager_buying_dep'] = Account(
            email='manager_buying_dep@test.test',
            password='manager_buying_dep',
            first_name=u'Илья',
            last_name=u'Швицман',
            department=self.demo_company_units['buying_dep'],
            job=self.demo_company_units['manager_buying_dep'],
        )
        self.demo_accounts['manager_buying_dep'].save()
        self.demo_accounts['manager_buying_dep'].set_password('manager_buying_dep')
        self.demo_accounts['manager_buying_dep'].save()

    def create_demo_tasks(self):
        template1 = TaskTemplate(
            title=u'Проанализировать продажи за месяц.',
            desc=u'Сравнить итоги с результатами прошлого месяца. Сравнить итоги с результатами такого же месяца прошлого года. Выявить менее продаваемые категории товаров.',
            author=self.demo_accounts['boss_sales_dep'],
            performer_unit=self.demo_company_units['boss_sales_dep'],
            performer=self.demo_accounts['boss_sales_dep'],
            due_date=datetime.datetime(self.next_month.year, self.next_month.month, 1, 11, 0),
            period=TaskTemplate.PERIOD_MONTH_BY_DAY,
        ).save()
        task1 = Task(
            template=template1,
            author=self.demo_accounts['boss_sales_dep'],
            due_date=datetime.datetime(self.next_month.year, self.next_month.month, 1, 11, 0),
        ).save()

    def create_demo_deal_statuses(self):
        DealStatus(
            pk='new',
            title=u'Новая'
        ).save()
        DealStatus(
            pk='wait_presentation',
            title=u'Ожидает презентации товара'
        ).save()
        DealStatus(
            pk='wait_client_answer_about_sale',
            title=u'Ожидает решения клиента по покупке'
        ).save()
        DealStatus(
            pk='close',
            title=u'Сделка завершена'
        ).save()

    def create_demo_companies(self):
        self.demo_companies = {}
        self.demo_companies['company1'] = Company(
            name=u'Компания 1',
            is_lead=True,
            author=self.demo_accounts['manager_sales_dep'],
        ).save()
        self.demo_companies['company2'] = Company(
            name=u'Компания 2',
            is_partner=True,
            author=self.demo_accounts['manager_sales_dep'],
        ).save()
        self.demo_companies['company3'] = Company(
            name=u'Компания 3',
            is_client=True,
            author=self.demo_accounts['manager_sales_dep'],
        ).save()

    def create_demo_contacts(self):
        Contact(
            full_name=u'Петушков Василий Петрович',
            phone='(8442)33-44-33',
            mobile_phone='8-900-900-00-00',
            company=self.demo_companies['company1'],
            is_lead=True,
            author=self.demo_accounts['manager_sales_dep'],
        ).save()
        Contact(
            full_name=u'Емельянов Сергей Иванович',
            phone='(8442)24-54-36',
            mobile_phone='8-900-934-22-11',
            company=self.demo_companies['company2'],
            is_partner=True,
            author=self.demo_accounts['manager_sales_dep'],
        ).save()
        Contact(
            full_name=u'Шивалова Ольга Васильевна',
            phone='(8442)34-24-33',
            mobile_phone='8-900-904-04-04',
            company=self.demo_companies['company3'],
            is_client=True,
            author=self.demo_accounts['manager_sales_dep'],
        ).save()

    def run(self, *args, **options):
        self.create_demo_company_units()
        self.create_demo_accounts()
        self.create_demo_companies()
        self.create_demo_contacts()
        self.create_demo_deal_statuses()
        self.create_demo_tasks()
