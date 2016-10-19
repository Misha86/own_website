from django import forms
from blog.models import Article
from navigation.models import Category
from django.utils.translation import ugettext_lazy as _


class SendMassageForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': _('введіть Ваш e-mail')}))
    massage = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'placeholder': _('введіть текст повідомлення для відправлення')}))

    def clean_massage(self):
        massage = self.cleaned_data['massage']
        num_words = len(massage.split())
        if num_words < 3:
            raise forms.ValidationError(_('Дуже мало слів!'))
        return massage


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['article_title',
                  'article_text',
                  'article_category',
                  'article_tag',
                  'article_image']

        widgets = {'article_title': forms.TextInput(attrs={'class': 'form-control', 'rows': 4,
                                                           'placeholder': _('введіть назва статті')}),
                   'article_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                                         'placeholder': _("введіть текст статті")}),
                   'article_category': forms.Select(attrs={'class': 'form-control', 'rows': 4}),
                   'article_tag': forms.SelectMultiple(attrs={'class': 'form-control', 'rows': 4})}