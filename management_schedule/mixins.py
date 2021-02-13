import calendar
from collections import deque
import datetime
import itertools
from .models import Schedule,Group,Friend
from django.db.models import Q
from accounts.models import CustomUser


class BaseCalendarMixin:
    """カレンダークラスの基底クラス　"""
    #0:月,1:火...
    first_weekday =6
    week_names = ['月', '火', '水', '木', '金', '土', '日']

    def setup_calendar(self):
        self._calendar = calendar.Calendar(self.first_weekday)

    def get_week_names(self):
        week_names = deque(self.week_names)
        week_names.rotate(-self.first_weekday)
        return week_names

class MonthCalendarMixin(BaseCalendarMixin):
    """月間カレンダーの機能を提供するMixin"""

    def get_previous_month(self, date):
        """前月を返す"""
        if date.month == 1:
            return date.replace(year=date.year-1, month=12, day=1)
        else:
            return date.replace(month=date.month-1, day=1)

    def get_next_month(self, date):
        """次月を返す"""
        if date.month == 12:
            return date.replace(year=date.year+1, month=1, day=1)
        else:
            return date.replace(month=date.month+1, day=1)

    def get_month_days(self, date):
        """その月の全ての日を返す"""
        return self._calendar.monthdatescalendar(date.year, date.month)

    def get_current_month(self):
        """現在の月を返す"""
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        if month and year:
            month = datetime.date(year=int(year), month=int(month), day=1)
        else:
            month = datetime.date.today().replace(day=1)
        return month

    def get_month_calendar(self):
        """月間カレンダー情報の入った辞書を返す"""
        self.setup_calendar()
        current_month = self.get_current_month()
        calendar_data = {
            'now': datetime.date.today(),
            'month_days': self.get_month_days(current_month),
            'month_current': current_month,
            'month_previous': self.get_previous_month(current_month),
            'month_next': self.get_next_month(current_month),
            'week_names': self.get_week_names(),
            'color':['table-danger','table-secondary','table-warning','table-primary','table-success','table-light','table-info'],
        }
        return calendar_data

class WeekCalendarMixin(BaseCalendarMixin):
    """週間カレンダーの機能を提供する"""

    def get_week_days(self):
        """その周のすべてを返す"""
        year  = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day   = self.kwargs.get('day')

        if year and month and day :
            date = datetime.date(year=int(year),month=int(month),day=int(day))
        else:
            date = datetime.date.today()

        for week in self._calendar.monthdatescalendar(date.year,date.month):
            if date in week:
                return week

    def get_week_calendar(self):
        """週間カレンダーの情報が入った辞書を返す"""
        self.setup_calendar()
        days  = self.get_week_days()
        first = days[0]
        last  = days[-1]
        calendar_date ={
            'now': datetime.date.today(),
            'week_days': days,
            'week_previous': first - datetime.timedelta(days=7),
            'week_next': first + datetime.timedelta(days=7),
            'week_names': self.get_week_names(),
            'week_first': first,
            'week_last': last,
            'color':['table-danger','table-secondary','table-warning','table-primary','table-success','table-light','table-info'],

            }
        return calendar_date

class WeekWithScheduleMixin(WeekCalendarMixin):
    """スケジュール付きの、週間カレンダーを提供するMixin"""

    def get_week_schedules(self, start, end, days):
        """それぞれの日とスケジュールを返す"""
        lookup = {
            # '例えば、date__range: (1日, 31日)'を動的に作る
            '{}__range'.format(self.date_field): (start, end)
        }
        # 例えば、Schedule.objects.filter(date__range=(1日, 31日)) になる
        queryset = self.model.objects.filter(owner=self.request.user).filter(**lookup)

         # {1日のdatetime: 1日のスケジュール全て, 2日のdatetime: 2日の全て...}のような辞書を作る
        day_schedules = {day: [] for day in days}
        for schedule in queryset:
            #日付を取り出す
            schedule_date = getattr(schedule, self.date_field)
            day_schedules[schedule_date].append(schedule)
        return day_schedules

    def get_week_calendar(self):
        #1週間分のカレンダーを取り出す
        calendar_context = super().get_week_calendar()
        calendar_context['week_day_schedules'] = self.get_week_schedules(
            calendar_context['week_first'],
            calendar_context['week_last'],
            calendar_context['week_days']
        )
        return calendar_context



class MonthWithScheduleMixin(MonthCalendarMixin):
    """スケジュール付きの、月間カレンダーを提供するMixin"""

    def get_month_schedules(self, start, end, days):
        """それぞれの日とスケジュールを返す"""
        lookup = {
            # '例えば、date__range: (1日, 31日)'を動的に作る
            '{}__range'.format(self.date_field): (start, end)
        }
        # 例えば、Schedule.objects.filter(date__range=(1日, 31日)) になる
        queryset = self.model.objects.filter(owner=self.request.user).filter(**lookup)

        # {1日のdatetime: 1日のスケジュール全て, 2日のdatetime: 2日の全て...}のような辞書を作る
        day_schedules = {day: [] for week in days for day in week}
        for schedule in queryset:
            schedule_date = getattr(schedule, self.date_field)
            day_schedules[schedule_date].append(schedule)

        # day_schedules辞書を、周毎に分割する。[{1日: 1日のスケジュール...}, {8日: 8日のスケジュール...}, ...]
        # 7個ずつ取り出して分割しています。
        size = len(day_schedules)
        return [{key: day_schedules[key] for key in itertools.islice(day_schedules, i, i+7)} for i in range(0, size, 7)]

    def get_month_calendar(self):
        calendar_context = super().get_month_calendar()
        month_days = calendar_context['month_days']
        month_first = month_days[0][0]
        print(month_first)
        month_last = month_days[-1][-1]
        calendar_context['month_day_schedules'] = self.get_month_schedules(
            month_first,
            month_last,
            month_days
        )
        return calendar_context








class MonthCalendarMixin3(BaseCalendarMixin):
    """月間カレンダーの機能を提供するMixin"""

    def get_previous_month(self, date):
        """前月を返す"""
        if date.month == 1:
            return date.replace(year=date.year-1, month=12, day=1)
        else:
            return date.replace(month=date.month-1, day=1)

    def get_next_month(self, date):
        """次月を返す"""
        if date.month == 12:
            return date.replace(year=date.year+1, month=1, day=1)
        else:
            return date.replace(month=date.month+1, day=1)

    def get_month_days(self, date):
        """その月の全ての日を返す"""
        return self._calendar.monthdatescalendar(date.year, date.month)

    def get_current_month(self,year,month):
        """現在の月を返す"""
        if month and year:
            month = datetime.date(year=int(year), month=int(month), day=1)
        else:
            month = datetime.date.today().replace(day=1)
        return month

    def get_month_calendar(self,year,month):
        """月間カレンダー情報の入った辞書を返す"""
        self.setup_calendar()
        current_month = self.get_current_month(year,month)
        calendar_data = {
            'now': datetime.date.today(),
            'month_days': self.get_month_days(current_month),
            'month_current': current_month,
            'month_previous': self.get_previous_month(current_month),
            'month_next': self.get_next_month(current_month),
            'week_names': self.get_week_names(),
            'color':['table-danger','table-secondary','table-warning','table-primary','table-success','table-light','table-info'],
        }
        return calendar_data





class MonthWithScheduleMixin3(MonthCalendarMixin3):
    """スケジュール付きの、月間カレンダーを提供するMixin"""

    def get_month_schedules(self,owner,group_list,start, end, days,year,month,name=None):
        """それぞれの日とスケジュールを返す"""
        lookup = {
            # '例えば、date__range: (1日, 31日)'を動的に作る
            '{}__range'.format('date'): (start, end)
        }
        print(lookup)

        # 例えば、Schedule.objects.filter(date__range=(1日, 31日)) になる
        if name == None:
            groups = Group.objects.filter(title__in=group_list)
            print(groups)
            #print(groups)
            #グループに含まれるfriendを所得
            me_friends = Friend.objects.filter(group__in=groups)
            print(me_friends)
            me_users = set()
            for f in me_friends:
                me_users.add(f.user)
                me_users.add(f.owner)

            me_users = list(me_users)
            his_groups = Group.objects.filter(owner__in=me_users)
            print(his_groups)
            his_friends = Friend.objects.filter(user=owner).filter(group__in=his_groups)
            me_groups = []
            for hf in his_friends:
                me_groups.append(hf.group)

            schedules = Schedule.objects.filter(Q(owner__in=me_users) | Q(owner=owner)).\
            filter(group__in=groups).filter(**lookup)

        else:
            print(name)
            #print(group_list)
            groups = Group.objects.filter(title__in=group_list)
            print(groups)
            users = CustomUser.objects.filter(username=name).first()
            #print(users)
            #print(groups)

            schedules = Schedule.objects.filter(owner=users).filter(group__in=groups).filter(**lookup)
            # {1日のdatetime: 1日のスケジュール全て, 2日のdatetime: 2日の全て...}のような辞書を作る
        day_schedules = {day: [] for week in days for day in week}
        for schedule in schedules:
            print(schedule)
            schedule_date = getattr(schedule, 'date')
            day_schedules[schedule_date].append(schedule)

        # day_schedules辞書を、周毎に分割する。[{1日: 1日のスケジュール...}, {8日: 8日のスケジュール...}, ...]
        # 7個ずつ取り出して分割しています。
        size = len(day_schedules)
        return [{key: day_schedules[key] for key in itertools.islice(day_schedules, i, i+7)} for i in range(0, size, 7)]

    def get_month_calendar(self,owner,group_list,year,month,name=None):
        calendar_context = super().get_month_calendar(year,month)
        month_days = calendar_context['month_days']
        month_first = month_days[0][0]
        print(month_first)
        month_last = month_days[-1][-1]
        calendar_context['month_day_schedules'] = self.get_month_schedules(
            owner,
            group_list,
            month_first,
            month_last,
            month_days,
            year,
            month,
            name,
        )
        return calendar_context









































class MonthCalendarMixin2(BaseCalendarMixin):
    """月間カレンダーの機能を提供するMixin"""

    def get_previous_month(self, date):
        """前月を返す"""
        if date.month == 1:
            return date.replace(year=date.year-1, month=12, day=1)
        else:
            return date.replace(month=date.month-1, day=1)

    def get_next_month(self, date):
        """次月を返す"""
        if date.month == 12:
            return date.replace(year=date.year+1, month=1, day=1)
        else:
            return date.replace(month=date.month+1, day=1)

    def get_month_days(self, date):
        """その月の全ての日を返す"""
        return self._calendar.monthdatescalendar(date.year, date.month)

    def get_current_month(self,year,month,day):
        """現在の月を返す"""
        month = month
        year = year
        if month and year:
            month = datetime.date(year=int(year), month=int(month), day=1)
        else:
            month = datetime.date.today().replace(day=1)
        return month

    def get_month_calendar(self,year,month,day):
        """月間カレンダー情報の入った辞書を返す"""
        self.setup_calendar()
        current_month = self.get_current_month(year,month,day)
        calendar_data = {
            'now': datetime.date.today(),
            'month_days': self.get_month_days(current_month),
            'month_current': current_month,
            'month_previous': self.get_previous_month(current_month),
            'month_next': self.get_next_month(current_month),
            'week_names': self.get_week_names(),
            'color':['table-danger','table-secondary','table-warning','table-primary','table-success','table-light','table-info'],
        }
        return calendar_data


class MonthWithScheduleMixin2(MonthCalendarMixin2):
    """スケジュール付きの、月間カレンダーを提供するMixin"""

    def get_month_schedules(self, user,start, end, days):
        """それぞれの日とスケジュールを返す"""
        lookup = {
            # '例えば、date__range: (1日, 31日)'を動的に作る
            '{}__range'.format('date'): (start, end)
        }
        # 例えば、Schedule.objects.filter(date__range=(1日, 31日)) になる
        queryset = Schedule.objects.filter(owner=user).filter(**lookup)

        # {1日のdatetime: 1日のスケジュール全て, 2日のdatetime: 2日の全て...}のような辞書を作る
        day_schedules = {day: [] for week in days for day in week}
        for schedule in queryset:
            schedule_date = getattr(schedule,'date')
            day_schedules[schedule_date].append(schedule)

        # day_schedules辞書を、周毎に分割する。[{1日: 1日のスケジュール...}, {8日: 8日のスケジュール...}, ...]
        # 7個ずつ取り出して分割しています。
        size = len(day_schedules)
        return [{key: day_schedules[key] for key in itertools.islice(day_schedules, i, i+7)} for i in range(0, size, 7)]

    def get_month_calendar(self,user,year,month,day):
        calendar_context = super().get_month_calendar(year,month,day)
        month_days = calendar_context['month_days']
        month_first = month_days[0][0]
        print(month_first)
        month_last = month_days[-1][-1]
        calendar_context['month_day_schedules'] = self.get_month_schedules(
            user,
            month_first,
            month_last,
            month_days
        )
        return calendar_context
