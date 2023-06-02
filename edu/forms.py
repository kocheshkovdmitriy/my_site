from edu import models
from django import forms

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ["task", "answer", "section"]

class AnswerForm(forms.Form):
    answer=forms.CharField(max_length=100, label='Ваш ответ:')