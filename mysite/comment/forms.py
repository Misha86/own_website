from comment.models import Comments
from django import forms
from django.utils.translation import ugettext_lazy as _


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comments_text']
        widgets = {'comments_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})}
        labels = {'comments_text': _('Введіть текст коментаря')}
        error_messages = {'comments_text': {'max_length': _('Даний коментар дуже довгий.')}, }

    def clean_comments_text(self):
        comments_text = self.cleaned_data['comments_text']
        num_words = len(comments_text.split())
        if num_words < 4:
            raise forms.ValidationError(_('Дуже мало слів!'))
        return comments_text

