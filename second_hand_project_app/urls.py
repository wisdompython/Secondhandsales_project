from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView , QUesAns, process_negotiation
from .views import view_negotiations, negotiation, order_view,update_cart, checkout, process_order, purchase_history,completed_nego

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('product/<pk>', ProductDetailView.as_view(), name='product-detail'),
    path('product_create/', ProductCreateView.as_view(), name='new_product'),
    path('product_update/<pk>', ProductUpdateView.as_view(), name='update_product'),
    path('orders/', order_view, name='orders'),
    path('update_cart/', update_cart, name='update_cart'),
    path('checkout/', checkout, name='checkout'),
    path('process-order/', process_order, name='process-order'),
    path('purchase-history/', purchase_history, name='purchase-history'),
    path('QA_section/<id>', QUesAns, name='QA-section'),
    path('nego_results/<id>', negotiation, name='nego_results'),
    path('nego/', view_negotiations, name='negotiations'),
    path('nego_complete/', completed_nego ,name='negotiation-complete'),
    path('process-negotiation/', process_negotiation, name='process-negotiation'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)