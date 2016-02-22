from django import forms
from product.models import Comment, Product


class CommentForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(),
                                     widget=forms.HiddenInput())

    class Meta:
        model = Comment
        fields = ['user', 'email', 'comment', 'product']
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(
                              attrs={'cols': '4', 'rows': '3',
                                     'class': 'content form-control'})
        }
