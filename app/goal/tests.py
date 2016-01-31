# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse_lazy
from model_mommy import mommy

from .models import Goal
from .forms import GoalForm
from app.account.models import Account, CompanyUnit
from app.core.helpers import DemoData

class TestGoal(TestCase):
    def setUp(self, *args, **kwargs):
        super(TestGoal, self).setUp(*args, **kwargs)
        demo = DemoData()
        demo.run()
        self.accounts = {
            'boss_sales_dep': Account.objects.get(email='boss_sales_dep@test.test'),
            'director': Account.objects.get(email='director@test.test'),
        }
        self.today = datetime.date.today()
        self.user = self.accounts['boss_sales_dep']
        self.login()
    
    def login(self):
        self.client.login(username='boss_sales_dep@test.test', password='boss_sales_dep')

    def create_test_goals(self):
        self.test_goals = []
        # создаем две тестовые цели
        test_title1 = 'test goal 1'
        test_desc1 = 'desc goal 1'
        # цель авторизованного сотрудника
        g1 = Goal(
            title=test_title1,
            desc=test_desc1,
            date_from=self.today - datetime.timedelta(days=10),
            date_to=self.today + datetime.timedelta(days=30),
            author=self.user,
        )
        g1.save()
        g1.performers = CompanyUnit.objects.filter(account_of_job=self.user)
        g1.save()
        self.test_goals.append(g1)

        test_title2 = 'test goal 2'
        test_desc2 = 'desc goal 2'
        # цель любого другого сотрудника, кроме авторизованного
        g2 = Goal(
            title=test_title2,
            desc=test_desc2,
            date_from=self.today - datetime.timedelta(days=10),
            date_to=self.today + datetime.timedelta(days=30),
            author=self.accounts['boss_sales_dep'],
        )
        g2.save()
        g2.performers = CompanyUnit.objects.filter(pk__in=(2,5))
        g2.save()
        self.test_goals.append(g2)

        test_title3 = 'test goal 3'
        test_desc3 = 'desc goal 3'
        # цель любого другого сотрудника, кроме авторизованного
        g3 = Goal(
            title=test_title3,
            desc=test_desc3,
            date_from=self.today - datetime.timedelta(days=12),
            date_to=self.today + datetime.timedelta(days=20),
            author=self.accounts['boss_sales_dep'],
        )
        g3.save()
        self.test_goals.append(g3)

        test_title4 = 'test goal 4'
        test_desc4 = 'desc goal 4'
        # цель любого другого сотрудника, кроме авторизованного
        g4 = Goal(
            title=test_title4,
            desc=test_desc4,
            date_from=self.today - datetime.timedelta(days=14),
            date_to=self.today + datetime.timedelta(days=24),
            author=self.accounts['boss_sales_dep'],
        )
        g4.save()
        g4.performers.add(self.accounts['boss_sales_dep'].department)
        g4.save()
        self.test_goals.append(g4)

    def test_goal_model(self):
        self.create_test_goals()
        self.assertTrue(isinstance(self.test_goals[0], Goal))
        self.assertEqual(self.test_goals[0].title, self.test_goals[0].__unicode__())
        self.assertTrue(isinstance(self.test_goals[1], Goal))
        self.assertEqual(self.test_goals[1].title, self.test_goals[1].__unicode__())

    def test_post_goal(self):
        # self.prepare()

        self.assertEqual(getattr(Account.objects.get(email='director@test.test'), 'email', None), 'director@test.test')

        test_title = 'test goal post'
        test_desc = 'desc goal'
        response = self.client.post(reverse_lazy('goal:add_goal_page'), {
            'title': test_title,
            'desc': test_desc,
            'date_from': (self.today - datetime.timedelta(days=10)).strftime('%d.%m.%Y'),
            'date_to': (self.today + datetime.timedelta(days=20)).strftime('%d.%m.%Y'),
            'performers': (2,5,),
            'author': self.user.pk,
        })
        #from django.utils.encoding import smart_unicode
        g = Goal.objects.get(title=test_title)
        desc = getattr(g, 'desc', None)
        self.assertEqual(desc, test_desc)
        g.delete()

    def test_goals_view(self):
        self.create_test_goals()
        # открываем страницу со списком целей авторизованного сотрудника
        response = self.client.get(reverse_lazy('goal:my_goals_list_page'))
        # проверяем статус ответа
        self.assertEqual(response.status_code, 200)
        # проверяем есть ли заголовок цели авторизованного сотрудника
        self.assertContains(response, self.test_goals[0].title)
        # проверяем нет ли цели другого сотрудника
        self.assertNotContains(response, self.test_goals[1].title)

        response = self.client.get(reverse_lazy('goal:company_goals_list_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_goals[2].title)
        self.assertNotContains(response, self.test_goals[0].title)
        self.assertNotContains(response, self.test_goals[1].title)

        response = self.client.get(reverse_lazy('goal:department_goals_list_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_goals[3].title)
        self.assertNotContains(response, self.test_goals[0].title)
        self.assertContains(response, self.test_goals[1].title)
        self.assertNotContains(response, self.test_goals[2].title)

        response = self.client.get(reverse_lazy('goal:goal_detail_page', kwargs={'pk': self.test_goals[0].pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_goals[0].desc)

    def test_goal_form(self):
        g4_title = 'test goal 4 title'
        g4_desc = 'test goal 4 desc'
        request = self.client.get(reverse_lazy('goal:add_goal_page'))
        form = GoalForm({
            'title': g4_title,
            'desc': g4_desc,
            'date_from': (self.today - datetime.timedelta(days=10)).strftime('%d.%m.%Y'),
            'date_to': (self.today + datetime.timedelta(days=10)).strftime('%d.%m.%Y'),
            'author': self.user.pk,
        }, request=request.wsgi_request)
        self.assertTrue(form.is_valid())
