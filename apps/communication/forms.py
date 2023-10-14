from django import forms
from django.template.context_processors import request

from .models import Messages
from apps.product.models import Comments

from django import forms
from mptt.forms import TreeNodeChoiceField


class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comments.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comments
        fields = ('made_by', 'name', 'email', 'made_on', 'parent', 'content')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', "required": False}),
            'email': forms.TextInput(attrs={'class': 'form-control', "required": False}),
            'content': forms.Textarea(attrs={'class': 'form-text-control', 'placeholder':'write a comment'}),
        }

    def save(self, *args, **kwargs):
        Comments.objects.rebuild()
        return super(NewCommentForm, self).save(*args, **kwargs)


class MessageForm(forms.ModelForm):
    content = forms.CharField(label='', max_length=255, help_text='Required', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Write your messages', 'id': 'login'
                                                                                       'edit-storename'}))
    class Meta:
        model= Messages
        fields=('content',)
