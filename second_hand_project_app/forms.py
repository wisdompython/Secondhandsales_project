from django import forms
from .models import OrderItem
from .models import Comment , Negotiation,QA
class NewOrder(forms.ModelForm):
    
    class Meta:
        model  = OrderItem
        fields = '__all__'


class ProductReviewForm(forms.ModelForm):
    body = forms.Textarea()
    class Meta:
        model = Comment
        fields = ['body']

class NegotiationForm(forms.ModelForm):
    class Meta:
        model = Negotiation
        fields = ['body']
class QAForm(forms.ModelForm):
    class Meta:
        model = QA
        fields = ['body']
    