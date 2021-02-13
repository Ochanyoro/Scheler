from .models import Schedule
from django import forms
from accounts.models import CustomUser
from.models import Group,Friend
from django.db.models import Q
from django import forms
from .models import Document


class DocumentForm(forms.Form):
    document = forms.FileField()
    def __init__(self, user, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.ChoiceField(
            choices=[('-','-')] + [(item.title, item.title) for item in Group.objects.filter(owner=user)],
            widget=forms.Select(attrs={'class':'form-control'}),
        )

class BS4ScheduleForm(forms.ModelForm):
    """Bootstrapに対応するためのModelForm"""

    class Meta:
        model = Schedule
        fields = ('summary', 'description', 'start_time', 'end_time','Nickname')
        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'start_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'end_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'Nickname': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_end_time(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        if end_time <= start_time:
            raise forms.ValidationError(
                '終了時間は、開始時間よりも後にしてください'
            )
        return end_time



class GroupCheckForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupCheckForm, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.ChoiceField(
            choices=list(set([(item.group.title, item.group.title) for item in Friend.objects.filter(user=user)]+[(item.title, item.title) for item in Group.objects.filter(owner=user)])),
            widget=forms.Select(),
        )

# Groupの選択メニューフォーム
class GroupSelectForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupSelectForm, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.ChoiceField(
            choices=[('-','-')] + [(item.title, item.title) for item in Group.objects.filter(owner=user)],
            widget=forms.Select(attrs={'class':'form-control'}),
        )



# Friendのチェックボックスフォーム
class FriendsForm(forms.Form):
    def __init__(self, user, friends=[], vals=[], *args, **kwargs):
        super(FriendsForm, self).__init__(*args, **kwargs)
        self.fields['friends'] = forms.MultipleChoiceField(
            choices=[(item.user, item.user) for item in friends],
            widget=forms.CheckboxSelectMultiple(),
            initial=vals
        )

# Group作成フォーム
class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control'}))

# 投稿フォーム
class PostForm(forms.Form):
    summary = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    start_time = forms.TimeField(widget=forms.TextInput(attrs={'class':'form-control'}))
    end_time = forms.TimeField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Nickname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}))

    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.ChoiceField(
            choices=list(set([(item.group.title, item.group.title) for item in Friend.objects.filter(user=user)]+[(item.title, item.title) for item in Group.objects.filter(owner=user)])),
            widget=forms.Select(),
        )


class PostForm2(forms.Form):
    summary = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    start_time = forms.TimeField(widget=forms.TextInput(attrs={'class':'form-control'}))
    end_time = forms.TimeField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Nickname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    def __init__(self, user, *args, **kwargs):
        super(PostForm2, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.ChoiceField(
            choices=list(set([(item.group.title, item.group.title) for item in Friend.objects.filter(user=user)]+[(item.title, item.title) for item in Group.objects.filter(owner=user)])),
            widget=forms.Select(),
        )





class EditForm(forms.ModelForm):
    """Bootstrapに対応するためのModelForm"""

    class Meta:
        model = Schedule
        fields = ('date','summary', 'description', 'start_time', 'end_time')
        widgets = {
            'date': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'summary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'start_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'end_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_end_time(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        if end_time <= start_time:
            raise forms.ValidationError(
                '終了時間は、開始時間よりも後にしてください'
            )
        return end_time

class AddFriend(forms.Form):
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    def __init__(self, user, *args, **kwargs):
        super(AddFriend, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.ChoiceField(
            choices=list(set([(item.group.title, item.group.title) for item in Friend.objects.filter(user=user)]+[(item.title, item.title) for item in Group.objects.filter(owner=user)])),
            widget=forms.Select(),
        )

class DeleteGroup(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(DeleteGroup, self).__init__(*args, **kwargs)
        self.fields['group_name'] = forms.ChoiceField(
            choices=list(set([(item.group.title, item.group.title) for item in Friend.objects.filter(owner=user)]+[(item.title, item.title) for item in Group.objects.filter(owner=user)])),
            widget=forms.Select(),
        )

class NameForm(forms.Form):
    last_name  = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

class Name2Nickname(forms.Form):
    last_name  = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    nickname   = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

class ChengeNickname(forms.Form):
    nickname   = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
