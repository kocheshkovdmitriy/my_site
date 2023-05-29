from django.forms import ModelForm
from core import models


class CommitForm(ModelForm):
    class Meta:
        model = models.Commit
        fields = ['user_name', 'description']
