from django.urls import path
from . import views

urlpatterns = [
        path('', views.index),
        path('newbrand', views.brand_form),
        path('newbrandsaved', views.brand_save),
        path('brandlist', views.brand_list),
        path('branddelete', views.brand_delete_form),
        path('branddeleted', views.brand_delete),
        path('newproduct', views.product_form),
        path('newproductsaved', views.product_save),
        path('productlist', views.product_list),
        path('productdelete', views.product_delete_form),
        path('productdeleted', views.product_delete),
        path('product-json/<str:brand_name>/', views.get_json_product_data),
        path('purchase', views.purchase_form),
        path('purchased', views.purchase),
        path('purchasehistory', views.purchase_history),
        path('sale', views.sale_form),
        path('sold', views.sale),
        path('salehistory', views.sale_history),
        path('credit', views.credit_form),
        path('credited', views.credit),
        path('credithistory', views.credit_history),
        ]
