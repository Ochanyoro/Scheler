import numpy as np
import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import timedelta
from django.db.models import Q
from django.views import generic
from . import mixins
from .forms import BS4ScheduleForm,PostForm,EditForm,PostForm2,GroupCheckForm,AddFriend,CreateGroupForm,DeleteGroup,DocumentForm,NameForm,Name2Nickname,ChengeNickname
from .models import Schedule,Group,Friend,Good,Document,UserNickname
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from accounts.models import CustomUser
import xlrd
import pprint

# Create your views here.
class IView(generic.TemplateView):
    template_name = "base/index.html"

class MonthCalendar(LoginRequiredMixin,mixins.MonthCalendarMixin, generic.TemplateView):
    """月間カレンダーを表示するビュー"""
    template_name = 'schedule/month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class WeekCalendar(LoginRequiredMixin,mixins.WeekCalendarMixin, generic.TemplateView):
    """週間カレンダーを表示するビュー"""
    template_name = 'schedule/week.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context


class WeekWithScheduleCalendar(LoginRequiredMixin,mixins.WeekWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの週間カレンダーを表示するビュー"""
    template_name = 'schedule/week_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context

class MonthWithScheduleCalendar(LoginRequiredMixin,mixins.MonthWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの月間カレンダーを表示するビュー"""
    template_name = 'schedule/month_with_schedule2.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class MyCalendar(LoginRequiredMixin,mixins.MonthWithScheduleMixin, mixins.WeekWithScheduleMixin, generic.CreateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = 'schedule/mycalendar.html'
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        return context

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year  = self.kwargs.get('year')
        day   = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.user = self.request.user
        schedule.date = date
        schedule.save()
        return redirect('schedule:mycalendar', year=date.year, month=date.month, day=date.day)

class MyCalendarDetail(LoginRequiredMixin,generic.ListView):
    """その日の詳細なスケジュールを表示"""
    model = Schedule
    context_object_name = 'schedule_list'
    template_name ='schedule/mycalendar_detail.html'

    def get_queryset(self):
        """自分の情報を取得"""
        month = self.kwargs.get('month')
        year  = self.kwargs.get('year')
        day   = self.kwargs.get('day')


        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        context = Schedule.objects.filter(owner=self.request.user,date=date).order_by('start_time')
        return context

def GroupCalendarDetail(request,year=None,month=None,day=None,glist=None,name=None):
    glist = glist.replace("'",'')
    glist = glist.replace('[','')
    glist = glist.replace(']','')
    gglist = []
    gglist.append(glist)
    if year and month and day:
        date = datetime.date(year=int(year), month=int(month), day=int(day))
    else:
        date = datetime.date.today()

    if name == None:
        groups = Group.objects.filter(title__in=gglist)
        #print(groups)
        #グループに含まれるfriendを所得
        me_friends = Friend.objects.filter(group__in=groups)
        me_users = set()
        for f in me_friends:
            me_users.add(f.user)
            me_users.add(f.owner)

        his_groups = Group.objects.filter(owner__in=me_users)
        his_friends = Friend.objects.filter(user=request.user).filter(group__in=his_groups)
        me_groups = []
        me_users.add(request.user)
        members = list(me_users)
        for hf in his_friends:
            me_groups.append(hf.group)
        schedule=[]
        schedules_indi =None
        user = None
        for m in me_users:
            schedule.append(Schedule.objects.filter(owner=m).\
            filter(group__in=groups).filter(date=date).order_by('start_time'))
        params = {
            'schedule_list':schedule,
            'schedules_indi':schedules_indi,
            'members':members,
            'date':date,
            'users':user
        }
        print("MSMMKO")
        return render(request, 'schedule/group_calendar_detail.html', params)

    else:
        schedule=None
        members =None
        groups = Group.objects.filter(title__in=gglist)
        user = CustomUser.objects.filter(username=name).first()
        print("MSMMKO00000000000000000LK")
        username = user.username
        schedules_indi = Schedule.objects.filter(owner=user).filter(group__in=groups).filter(date=date).order_by('start_time')

        print(schedule)
        params = {
            'schedule_list':schedule,
            'schedules_indi':schedules_indi,
            'members':members,
            'date':date,
            'users':user,
            'glist':glist,
        }
        return render(request, 'schedule/today_schedule.html', params)




# メッセージのポスト処理
def createschedule(request,year=None,month=None,day=None):
    # POST送信の処理

    if request.method == 'POST':
        msg = Schedule()
        if year and month and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
            msg.date = date
        else:
            date = request.POST['date']
            msg.date =date
            d = date.split("-")
            year = d[0]
            month = d[1]
            day = d[2]
        # 送信内容の取得
        gr_name = request.POST['groups']
        summary = request.POST['summary']
        description = request.POST['description']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        Nickname = request.POST['Nickname']

        group = Group.objects.filter(title=gr_name).first()
        if group == None:
            (pub_user, group) = get_public()

        # Messageを作成し設定して保存
        msg.owner = request.user
        msg.group = group
        msg.summary = summary
        msg.description = description
        msg.start_time = start_time
        msg.end_time = end_time
        msg.Nickname = Nickname
        msg.save()
        # メッセージを設定
        messages.success(request, '新しいメッセージを投稿しました！')
        return redirect('schedule:today_schedule', year=int(year), month=int(month), day=int(day))

    # GETアクセス時の処理
    else:
        mouthwith = mixins.MonthWithScheduleMixin2()
        calendar_context = mouthwith.get_month_calendar(request.user,year,month,day)

        if year and month and day:
            form = PostForm2(request.user)
            date = datetime.date(year=int(year), month=int(month), day=int(day))
            params = {
                'login_user':request.user,
                'form':form,
                'date':date,
            }
        else:
            form = PostForm(request.user)
            params = {
                'login_user':request.user,
                'form':form,
            }
        params.update(calendar_context)
    return render(request, 'schedule/create_schedule.html', params)


class EditSchedule(LoginRequiredMixin,generic.UpdateView):
    """スケジュールの更新"""
    model = Schedule
    template_name = 'schedule/edit_schedule.html'
    form_class = EditForm

    def get_success_url(self):
        return reverse_lazy('schedule:today_schedule',kwargs={'year':self.kwargs['year'],'month':self.kwargs['month'],'day':self.kwargs['day']})

    def form_valid(self,form):
        messages.success(self.request,'スケジュールを編集しました')
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.error(self.request,'スケジュールの更新に失敗しました')
        return super().form_valid(form)

class DeleteSchedule(LoginRequiredMixin,generic.DeleteView):
    model =Schedule
    template_name = "schedule/delete_schedule.html"


    def get_success_url(self):
        return reverse_lazy('schedule:today_schedule',kwargs={'year':self.kwargs['year'],'month':self.kwargs['month'],'day':self.kwargs['day']})

    def delete(self,request,*args,**kwargs):
        messages.success(self.request,'予定を削除しました')
        return super().delete(request,*args,**kwargs)





#汚いがここでは選択されたグループに属しているschesuleを取得
def selectGroup(request,year=None,month=None,glist=None,name=None):

    if request.method == 'POST':
        glist = []
        for item in request.POST.getlist('groups'):
            glist.append(item)
        print(glist)
        #選択されたグループの中に含まれている人のscheduleを抜き出す
        date = datetime.date.today()

        mouthwith = mixins.MonthWithScheduleMixin3()
        calendar_context = mouthwith.get_month_calendar(request.user,glist,date.year,date.month)

        params = {
            'glist':glist
        }
        params.update(calendar_context)
        return render(request,'schedule/month_with_schedule4.html',params)

    else :
        if glist == None:

            checkform = GroupCheckForm(request.user)
            params = {
                'login_user':request.user,
                'checkform':checkform,
            }
        else:
            glist = glist.replace("'",'')
            glist = glist.replace('[','')
            glist = glist.replace(']','')
            gglist = []
            gglist.append(glist)
            print(gglist)
            if year and month :
                date = datetime.date(year=int(year), month=int(month), day=1)
            else:
                date = datetime.date.today()
            mouthwith = mixins.MonthWithScheduleMixin3()
            if name==None:
                calendar_context = mouthwith.get_month_calendar(request.user,gglist,date.year,date.month)
                params = {
                    'glist':gglist,
                }
                print('うんこ')
            else:
                params = {
                    'glist':gglist,
                    'name':name,
                    'users':name,
                }
                calendar_context = mouthwith.get_month_calendar(request.user,gglist,date.year,date.month,name)
                print(name)
                print('unnko')
            params.update(calendar_context)
            return render(request,'schedule/month_with_schedule4.html',params)

        return render(request,'schedule/select_group.html',params)

def display_member(request,glist):
    glist = glist.replace("'",'')
    glist = glist.replace('[','')
    glist = glist.replace(']','')
    gglist = []
    gglist.append(glist)
    groups = Group.objects.filter(title__in=gglist)
    #print(groups)
    #グループに含まれるfriendを所得
    me_friends = Friend.objects.filter(group__in=groups)
    me_users = set()
    for f in me_friends:
        me_users.add(f.user)
        me_users.add(f.owner)

    me_users.add(request.user)
    members = list(me_users)
    members = CustomUser.objects.filter(username__in = members)
    print(members)
    params = {
        'members':members,
        'glist':gglist,
        'm':glist,
    }
    return render(request,'schedule/list_member.html',params)

def nukeru_group(request,glist,id):
    glist = glist.replace("'",'')
    glist = glist.replace('[','')
    glist = glist.replace(']','')
    gglist = []
    gglist.append(glist)
    groups = Group.objects.filter(title__in=gglist).first()
    print(groups)
    user = CustomUser.objects.filter(id=id).first()
    print(user)
    friend = Friend.objects.filter(user=user).filter(group=groups).first()
    if str(request.user) == str(user.username):
        return redirect("schedule:select_group")
    friend.delete()
    s = Schedule.objects.filter(owner=user).filter(group=groups)
    s.delete()
    messages.info(request,gglist[0]+"の"+user.username+"を削除しました")
    return redirect("schedule:display_member",glist)



#友達の追加
def addFriends(request,glist=None):
    if request.method == "POST":
        gglist = []
        if glist :
            glist = glist.replace("'",'')
            glist = glist.replace('[','')
            glist = glist.replace(']','')
            gglist.append(glist)

        last_name = request.POST['last_name']
        first_name= request.POST['first_name']
        nickname  = request.POST['nickname']
        group = request.POST['groups']
        group = Group.objects.filter(title=group).filter(owner=request.user).first()
        add_user = CustomUser.objects.filter(last_name=last_name).filter(first_name=first_name).first()
        print(add_user)
        nickname_user = UserNickname.objects.filter(owner = add_user).first()
        print(nickname_user)
        if nickname_user.nickname != nickname:
            messages.info(request,"ニックネームが違います")
            add_firend = AddFriend(request.user)
            params = {
                'login_user':request.user,
                'add_friend':add_firend,
                'glist':gglist
            }
            return render(request,'schedule/add_friend.html',params)
        if add_user == request.user:
            messages.info(request,"自分自身は追加できません")
            add_firend = AddFriend(request.user)
            params = {
                'login_user':request.user,
                'add_friend':add_firend,
                'glist':gglist
            }
            return render(request,'schedule/add_friend.html',params)
        f_num = Friend.objects.filter(owner=request.user).filter(user=add_user).filter(group=group).count()
        if f_num>0:
            messages.info(request,add_user.last_name+add_user.first_name+"はすでに追加されています")
            add_firend = AddFriend(request.user)
            params = {
                'login_user':request.user,
                'add_friend':add_firend,
                'glist':gglist,
            }
            return render(request,'schedule/add_friend.html',params)

        friend = Friend()
        friend.owner = request.user
        friend.user = add_user
        friend.group = group
        friend.save()
        messages.success(request,add_user.last_name+add_user.first_name+"を追加しました。")
        if glist :
            return redirect('schedule:display_member',gglist)
        else:
            return redirect('schedule:select_group')

    else:
        add_firend = AddFriend(request.user)
        gglist = []
        if glist:
            glist = glist.replace("'",'')
            glist = glist.replace('[','')
            glist = glist.replace(']','')
            gglist.append(glist)

        params = {
            'login_user':request.user,
            'add_friend':add_firend,
            'glist':gglist
        }
        return render(request,'schedule/add_friend.html',params)


#グループの追加
def createGroup(request):
    if request.method == 'POST':
        group = Group()
        group.owner = request.user
        group.title = request.user.last_name+request.user.first_name+"の"+request.POST['group_name']
        group.save()
        messages.info(request,'新しいグループを作成しました')
        return redirect('schedule:display_member',str(group.title))

    else:
        create_group = CreateGroupForm()
        params = {
            'create_group':create_group,
        }
        return render(request,'schedule/create_group.html',params)

def deleteGroup(request,id=None):
    if request.method == 'POST':
        group_name = request.POST['group_name']
        group = Group.objects.filter(title=group_name).first()
        a = str(group.owner.username)
        b = str(request.user)
        if a != b:
            messages.info(request,request.user.username+"はownerではないため削除することができません")
            return redirect("schedule:select_group")
        group.delete()
        messages.info(request,group_name+"を削除しました")
        return redirect("schedule:select_group")

    else:
        if id == None:
            delete_group = DeleteGroup(request.user)
            params = {
                'delete_group':delete_group,
            }
            return render(request,'schedule/delete_group.html',params)

        else:
            group = Group.objects.filter(id=id).first()
            print(group)
            print(group.owner.username)
            print(request.user)
            a = str(group.owner.username)
            b = str(request.user)
            if a != b:
                messages.info(request,request.user.username+"はownerではないため削除することができません")
                return redirect("schedule:list_group")
            group.delete()
            messages.info(request,group.title+"を削除しました")
            return redirect('schedule:list_group')

def listGroup(request):
    if request.method == 'POST':
        return redirect('schedule:select_group')
    else:
        friends = Friend.objects.filter(user=request.user)
        group_title = []
        for f in friends:
            group_title.append(f.group.title)
        group1 = Group.objects.filter(title__in=group_title)
        group2 = Group.objects.filter(owner=request.user)
        param = {
            'owner':request.user,
            'group1':group1,
            'group2':group2
        }
        return render(request,'schedule/list_group.html',param)


def comfirm(request,id):
    param ={
        'id':id
    }
    return render(request,'schedule/comfirm.html',param)

def comfirm_member(request,glist,id):
    param ={
        'id':id,
        'glist':glist
    }
    return render(request,'schedule/comfirm_member.html',param)



def input_excel(request):
    if request.method == 'POST':
        glist = []
        for item in request.POST.getlist('groups'):
            glist.append(item)
        group = Group.objects.filter(title__in=glist).first()
        file  = request.FILES["document"]
        docu = Document()
        docu.description =group
        docu.document = file
        docu.save()

        ex = Document.objects.filter(description=group).first()
        wb = xlrd.open_workbook('.'+str(ex.document.url))
        sheet = wb.sheet_by_name('Sheet1')
        l_2d_all = get_list_2d_all(sheet)
        #天地にしている
        l_2d_all = np.array(l_2d_all).T
        name_list =[]
        #名前のみを抽出する
        for i in range(2,len(l_2d_all[0])):
            if l_2d_all[0][i] != "":
                name_list.append(l_2d_all[0][i])
        print(name_list)
        weekname = ["火","水","木","金","土","日"]
        weekkoma =[3,3,3,3,6,6]

        kari = []
        l_2d_all = l_2d_all.T
        print(l_2d_all.shape)
        schedule={}
        for i in range(0,len(name_list)):
            a=0
            people ={}
            for week in range(0,len(weekname)):
                now =[]
                for j in range(0,weekkoma[week]):
                    a=a+1
                    people_kari =[]
                    student = []
                    content = []
                    if l_2d_all[i*4+2][a] != "":
                        #print(l_2d_all[i*4+1][a])
                        student.append(l_2d_all[i*4+2][a])
                        content.append(l_2d_all[i*4+3][a])
                        people_kari.append(student)
                        people_kari.append(content)
                    if l_2d_all[i*4+4][a] != "":
                        #print(l_2d_all[i*4+3][a])
                        student.append(l_2d_all[i*4+4][a])
                        content.append(l_2d_all[i*4+5][a])
                        people_kari.append(student)
                        people_kari.append(content)
                    #print(student)
                    #print(people_kari)
                    now.append(people_kari)
                    #print(now)
                people[weekname[week]] = now
            schedule[name_list[i]] = people
        x =excel_date(int(float(l_2d_all[0][0])))

        normal =datetime.datetime(2021, 1, 1, 12, 45, 0)
        zikan =["A","B","C","D","E","F"]
        gp = Group.objects.filter(title__in=glist).first()
        me_friends = Friend.objects.filter(group=group)
        print(me_friends)
        me_users = set()
        me_users.add(request.user.last_name)
        for f in me_friends:
            me_users.add(f.user.last_name)
            me_users.add(f.owner.last_name)

        me_users = list(me_users)
        print(me_users)

        for name in name_list:
            if name in me_users:
                people = schedule[name]
                now_user = CustomUser.objects.filter(last_name=name).first()
                j=0
                for week in weekname:
                    day_schedule = people[week]
                    i=0
                    k=3
                    for koma in day_schedule:
                        if week == "土" or week == "日":
                            if koma!=[]:
                                sc =Schedule()
                                sc.owner = now_user
                                sc.group = gp
                                sc.Nickname = name
                                sc.summary = zikan[i]
                                if len(koma[0]) == 2:
                                    sc.description = koma[0][0]+":"+koma[1][0]+koma[0][1]+":"+koma[1][1]
                                else:
                                    sc.description = koma[0][0]+":"+koma[1][0]
                                sc.start_time = (normal + timedelta(seconds=5400*(i))).time()
                                sc.end_time   = (normal + timedelta(seconds=5400*(1+i)) - timedelta(minutes=10)).time()
                                sc.date = x + timedelta(days = 1*j)
                                sc.save()
                            i=i+1
                        else :
                            if koma!=[]:
                                sc =Schedule()
                                sc.owner = now_user
                                sc.group = gp
                                sc.Nickname = name
                                sc.summary = zikan[k]
                                if len(koma[0]) == 2:
                                    sc.description = koma[0][0]+":"+koma[1][0]+"   "+koma[0][1]+":"+koma[1][1]
                                else:
                                    sc.description = koma[0][0]+":"+koma[1][0]
                                sc.start_time = (normal + timedelta(seconds=5400*(k))).time()
                                sc.end_time   = (normal + timedelta(seconds=5400*(1+k)) - timedelta(minutes=10)).time()
                                sc.date = x + timedelta(days = 1*j)
                                sc.save()
                            k=k+1
                    j=j+1

        return redirect('schedule:list_group')
    else:
        form = DocumentForm(request.user)
        return render(request, 'schedule/input_excel.html', {
            'form': form
        })


def excel_date(num):
    date = (datetime.datetime(1899, 12, 30) + timedelta(days=num)).date()
    return date

def schedule_input():
    pass


def get_list_2d_all(sheet):
    return [sheet.row_values(row) for row in range(sheet.nrows)]


def username_input(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name  = request.POST['last_name']
        user = request.user
        customuser = CustomUser.objects.filter(username=str(user)).first()
        customuser.first_name = first_name
        customuser.last_name  = last_name
        customuser.save()
        params = {
            'user':customuser,
        }
        return render(request,'schedule/index.html',params)
    else:
        form = NameForm()
        params = {
            'form':form
        }
        return render(request,'schedule/name_input.html',params)

def username_input_nickname(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name  = request.POST['last_name']
        nickname   = request.POST['nickname']
        user = request.user
        customuser = CustomUser.objects.filter(username=str(user)).first()
        customuser.first_name = first_name
        customuser.last_name  = last_name
        customuser.save()
        print(customuser)
        user_nickname = UserNickname()
        user_nickname.nickname = str(nickname)
        user_nickname.owner = customuser
        user_nickname.save()
        params = {
            'user':customuser,
        }
        return render(request,'schedule/index.html',params)
    else:
        form = Name2Nickname()
        params = {
            'form':form
        }
        return render(request,'schedule/name_input_nickname.html',params)

def chenge_nickname(request):
    if request.method == 'POST':
        nickname = request.POST['nickname']
        customuser = CustomUser.objects.filter(username=str(request.user)).first()
        nick = UserNickname.objects.filter(owner = customuser).first()
        nick.nickname = nickname
        nick.save()
        messages.info(request,"ニックネームを変更しました")
        return redirect('schedule:index')
    else:
        form = ChengeNickname()
        params = {
            'form':form
        }
        return render(request,'schedule/chenge_nickname.html',params)
