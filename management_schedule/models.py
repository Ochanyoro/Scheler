from django.db import models
import datetime
from django.utils import timezone
from accounts.models import CustomUser

# Create your models here.
class Schedule(models.Model):
    """スケジュールクラス"""
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='schedule_owner') #related_nameは逆参照をするため
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    Nickname = models.CharField('ニックネーム',max_length=10)
    summary = models.CharField('概要', max_length=50)
    description = models.TextField('詳細な説明', blank=True)
    start_time = models.TimeField('開始時間', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('終了時間', default=datetime.time(7, 0, 0))
    date = models.DateField('日付')
    good_count = models.IntegerField(default=0)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return str(self.summary) + '(' + str(self.owner) + ')'

class UserNickname(models.Model):
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=150,unique=True)

    def __str__(self):
        return '<' + str(self.nickname) + '(' + str(self.owner) +')>'


class Group(models.Model):
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='group_owner')
    title= models.CharField(max_length=20)

    def __str__(self):
        return '<' + str(self.title) + '(' + str(self.owner) +')>'

class Friend(models.Model):
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='friend_owner')
    user  = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + '(group:"' + str(self.group) + '")'

class Good(models.Model):
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='good_owner')
    schedule = models.ForeignKey(Schedule,on_delete=models.CASCADE)

    def __str__(self):
        return 'good for"' + str(self.schedule) + '"(by' + str(self.owner) + ')'

class Document(models.Model):
    description = models.ForeignKey(Group,on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
