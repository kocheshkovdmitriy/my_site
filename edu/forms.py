from edu import models
from django import forms

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ["task", "answer", "section"]