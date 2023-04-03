from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, ShippingAddress, Comment, Negotiation, QA
from .forms import ProductReviewForm, NegotiationForm, QAForm
import datetime
from django.db.models import  Q
from django.views import View
import json


class ProductListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_input = self.request.GET.get('Search') or ''
        if search_input:
            context['product'] = context['product'].filter(name__icontains=search_input)
            context['search_input'] = search_input

        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    queryset = Product.objects.all()
    context_object_name = 'product'

    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductReviewForm()
        context['comment'] = Comment.objects.filter(commentproduct=self.object.pk)
        return context

    def post(self, request, *args, **kwargs):
        form = ProductReviewForm()
        if not request.user.is_authenticated:
            return redirect('login')
        self.object = self.get_object()
        form = ProductReviewForm(request.POST)
        if form.is_valid:
            if not request.user.is_authenticated:
                return redirect('login')
            new_comment = form.save(commit=False)
            new_comment.commentproduct = Product.objects.get(pk=self.object.pk)
            new_comment.author = self.request.user
            new_comment.save()
            return redirect('product-detail', self.object.pk)
        else:
            form = ProductReviewForm()
        return redirect('product-list')


class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Product
    fields = ['name', 'description', 'features','reason_for_sale','condition','usage_duration',
    'size','category','image', 'price','is_digital']
    template_name = 'products/create_product.html'
    success_url = reverse_lazy('product-list')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'features','reason_for_sale','condition','usage_duration',
    'size','category','image', 'price','is_digital']
    template_name = 'products/update_product.html'
     
    

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            seller=self.request.user
        )

    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse_lazy('product-detail', kwargs={'pk':pk})


@login_required(login_url='login')
def order_view(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, completed=False)
        order_items = order.orderitem_set.all()
    else:
        return redirect('accounts/login')
    return render(request, 'products/order.html', {'order': order, 'order_items': order_items})


@login_required(login_url='login')
def update_cart(request):
    data = json.loads(request.body)  # load data from page
    product = Product.objects.get(id=data['productId'])
    action = data['action']
    order, created = Order.objects.get_or_create(customer=request.user, completed=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    # filter returns a list, get the element
    if action == 'add':  # if the action is add,  increment
        order_item.quantity = (order_item.quantity + 1)

    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()
        
    return JsonResponse('working', safe=False)


@login_required(login_url='login')
def checkout(request):
    order, created = Order.objects.get_or_create(customer=request.user, completed=False)
    order_summary = order.orderitem_set.all()

    return render(request, 'products/checkout.html', {'order_summary': order_summary, 'order': order})


@login_required(login_url='login')
def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()  # set a transaction id
    data = json.loads(request.body)
    # get total items from form
    order, created = Order.objects.get_or_create(customer=request.user, completed=False)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.completed = True
    order.save()

    if order.ship == True:
        ShippingAddress.objects.create(
            customer=request.user,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )

    return JsonResponse('good', safe=False)


@login_required(login_url='login')
def purchase_history(request):
    order_item = Order.objects.filter(customer=request.user, completed=True)

    return render(request, 'products/purchase_history.html', {'order_item': order_item})

@login_required(login_url='login')
def QUesAns(request, id):
    # get the product we are negotiating for
    product = Product.objects.get(id=id)
    QA_section = QA.objects.filter(product=product)
    QA_form = QAForm()
    if request.method == 'POST':
        QA_form = QAForm(request.POST)
        if QA_form.is_valid():
            QA_form_ = QA_form.save(commit=False)
            QA_form_.product = product
            QA_form_.author = request.user
            QA_form_.save()
            return redirect('QA-section', product.id)
        else:
            QA_form = QAForm()
    return render(request, 'products/QA_forum.html', {'qa_form': QA_form, 'QA_section': QA_section, 'product': product})

@login_required(login_url='login')
def negotiation(request, id):
    order_item = OrderItem.objects.get(id=id)  # order_item id
    nego_results = Negotiation.objects.filter(order_item=order_item).exists()  # negotiation results
    if nego_results:  # if a negotiation related with a order item exists, then you can go add and fill the form
        form = NegotiationForm()
        nego_results = Negotiation.objects.filter(order_item=order_item)
        form = NegotiationForm()
        if request.user == nego_results[0].order_item.product.seller:  # if the logged-in user is the owner of the
            # product, his replies will always go to a customer
            form = NegotiationForm()
            if request.method == 'POST':
                form = NegotiationForm(request.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.order_item = order_item
                    form.author = request.user
                    form.sent_to = nego_results[0].order_item.order.customer
                    form.save()

                    return redirect('nego_results', order_item.id)

        elif request.user == nego_results[0].order_item.order.customer:
            # if user is customer, he sends messages to the seller
            form = NegotiationForm()
            form = NegotiationForm()
            if request.method == 'POST':
                form = NegotiationForm(request.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.order_item = order_item
                    form.author = request.user
                    form.sent_to = nego_results[0].order_item.product.seller
                    form.save()
                    return redirect('nego_results', order_item.id)
        else:
            return redirect('product-list')

    else:
        Negotiation.objects.create(order_item=order_item, author=order_item.order.customer,
                                   sent_to=order_item.product.seller, body='I wanna discuss')
        nego_results = Negotiation.objects.filter(order_item=order_item)
        form = NegotiationForm()
        print('not working')
    context = {'nego_results': nego_results, 'form': form, 'order_item': order_item}
    return render(request, 'products/nego_results.html', context)

@login_required(login_url='login')
def view_negotiations(request):
    negotiation = Negotiation.objects.filter(Q(author=request.user, completed=False)|Q(sent_to=request.user, completed=False))
    return render(request, 'products/negotiation.html', {'negotiation': negotiation})
@login_required(login_url='login')
def completed_nego(request):
    negotiation = Negotiation.objects.filter(Q(author=request.user, completed=True)|Q(sent_to=request.user, completed=True))

    return render(request, 'products/nego_complete.html', {'negotiation': negotiation})



def process_negotiation(request):
    response = json.loads(request.body)
    order_item = OrderItem.objects.get(id=response['id'])
    nego_success = Negotiation.objects.filter(order_item=order_item)
    price = float(response['price'])
    order_item.agreed_price = price
    nego_success[0].completed = True
    nego_success[0].save()
    order_item.save()
    if order_item.agreed_price:
        for item in nego_success:
            item.completed = True
            item.save()
    return JsonResponse('sent', safe=False)