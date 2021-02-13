from django.urls import path

from . import views


app_name = 'schedule'
urlpatterns = [
    path('', views.IView.as_view(), name="index"),
    path('month/', views.MonthCalendar.as_view(), name='month'),
    path('month/<int:year>/<int:month>/', views.MonthCalendar.as_view(), name='month'),
    path('week/', views.WeekCalendar.as_view(), name='week'),
    path('week/<int:year>/<int:month>/<int:day>/', views.WeekCalendar.as_view(), name='week'),
    path('week_with_schedule/', views.WeekWithScheduleCalendar.as_view(), name='week_with_schedule'),
    path('week_with_schedule/<int:year>/<int:month>/<int:day>/',views.WeekWithScheduleCalendar.as_view(),name='week_with_schedule'),
    path('month_with_schedule/',views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'),
    path('month_with_schedule/<int:year>/<int:month>/',views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'),
    path('mycalendar/', views.MyCalendar.as_view(), name='mycalendar'),
    path('mycalendar/<int:year>/<int:month>/<int:day>/', views.MyCalendar.as_view(), name='mycalendar'),

    path('today_schedule/',views.MyCalendarDetail.as_view(),name="today_schedule"),
    path('today_schedule/<int:year>/<int:month>/<int:day>',views.MyCalendarDetail.as_view(),name="today_schedule"),
    path('create_schedule/',views.createschedule,name='create_schedule'),
    path('create_schedule/<int:year>/<int:month>/<int:day>',views.createschedule,name='create_schedule'),
    path('create_schedule/<int:year>/<int:month>',views.createschedule,name='create_schedule'),
    path('edit_schedule/<int:pk>/<int:year>/<int:month>/<int:day>',views.EditSchedule.as_view(),name='edit_schedule'),
    path('delete_schedule/<int:pk>/<int:year>/<int:month>/<int:day>/',views.DeleteSchedule.as_view(),name="delete_schedule"),



    path('select_group/',views.selectGroup,name="select_group"),
    path('select_group/<int:year>/<int:month>/<glist>',views.selectGroup,name="select_group"),
    path('select_group/<glist>',views.selectGroup,name="select_group"),
    path('select_group/<glist>/<name>',views.selectGroup,name="select_group"),
    path('select_group/<int:year>/<int:month>/<glist>/<name>/',views.selectGroup,name="select_group"),
    path('group_calendar_detail/<int:year>/<int:month>/<int:day>/<glist>',views.GroupCalendarDetail,name="group_calendar_detail"),
    path('group_calendar_detail/<glist>/<name>',views.GroupCalendarDetail,name="group_calendar_detail"),
    path('group_calendar_detail/<int:year>/<int:month>/<int:day>/<glist>/<name>/',views.GroupCalendarDetail,name="group_calendar_detail"),
    path('add_firends/',views.addFriends,name="add_friends"),
    path('add_firends/<glist>/',views.addFriends,name="add_friends"),
    path('create_group/',views.createGroup,name='create_group'),
    path('delete_group/',views.deleteGroup,name='delete_group'),
    path('delete_group/<id>/',views.deleteGroup,name='delete_group'),
    path('display_member/<glist>/',views.display_member,name="display_member"),
    path('nukeru_group/<glist>/<int:id>',views.nukeru_group,name="nukeru_group"),
    path('list_group/',views.listGroup,name="list_group"),
    path('comfirm/<id>',views.comfirm,name="comfirm"),
    path('comfirm_member/<glist>/<id>',views.comfirm_member,name="comfirm_member"),
    path('input_excel',views.input_excel,name="input_excel"),
    #path('output_excel',views.output_excel,name="output_excel"),
    path('username_input',views.username_input,name="username_input"),
    path('username_input_nickname',views.username_input_nickname,name="username_input_nickname"),
    path('chenge_nickname',views.chenge_nickname,name="chenge_nickname"),
]
