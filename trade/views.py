from django.shortcuts import render, redirect
from .models import Brand, Product, Purchase, Sale, Credit
from django.contrib import messages
from django.http import JsonResponse, HttpResponse

def index(request):
    return render(request, 'index.html')


def brand_form(request):
    return render(request, 'brand_entry.html')

def brand_save(request):
    b = request.POST['brand']
    try:
        Brand.objects.get(bname=b)
        messages.info(request,'brand already exists')
        return redirect('/trade/newbrand')
    except Brand.DoesNotExist:
        Brand.objects.create(bname=b)
        messages.info(request,'brand saved')
        return redirect('/trade/brandlist')

def brand_list(request):
    b = Brand.objects.all()
    return render(request, 'brand_list.html', {'brands': b})

def brand_delete_form(request):
    b = Brand.objects.all()
    return render(request, 'brand_delete.html', {'brands': b})

def brand_delete(request):
    Brand.objects.filter(bname=request.POST['brand_name']).delete()
    return redirect('/trade/brandlist')


def product_form(request):
    b = Brand.objects.all()
    return render(request, 'product_entry.html', {'brands': b})

def product_save(request):
    b = Brand.objects.get(bname=request.POST['brand_name'])
    pn = request.POST['product_name']
    ps = request.POST['product_size']
    try:
        Product.objects.get(bname=b,name=pn,size=ps)
        messages.info(request,'product already exists')
        return redirect('/trade/newproduct')
    except Product.DoesNotExist:
        Product.objects.create(bname=b,name=pn,size=ps)
        messages.info(request,'product saved')
        return redirect('/trade/productlist')

def product_list(request):
    p = Product.objects.all()
    return render(request, 'product_list.html', {'products': p})

def product_delete_form(request):
    b = Brand.objects.all()
    return render(request, 'product_delete.html', {'brands': b})

def product_delete(request):
    b = Brand.objects.filter(bname=request.POST['brand_name'])
    p = request.POST['product_name']
    s = request.POST['product_size']
    Product.objects.filter(bname=b[0].id,name=p,size=s).delete()
    return redirect('/trade/productlist')


def get_json_product_data(request, *args, **kwargs):
    selected_brand = kwargs.get('brand_name')
    obj_product = list(Brand.objects.get(bname=selected_brand).product_set.all().values())
    #obj_product_unique_name = list({v['name']:v for v in obj_product}.values())
    print(obj_product)
    return JsonResponse({'data':obj_product})


def purchase_form(request):
    b = Brand.objects.all()
    return render(request, 'purchase.html', {'brands': b})

def purchase(request):
    b = Brand.objects.get(bname=request.POST['brand_name'])
    pn = request.POST['product_name']
    ps = request.POST['product_size']
    p = Product.objects.get(bname=b,name=pn,size=ps)
    r = request.POST['rate']
    q = request.POST['quantity']
    n = request.POST['notes']
    uq = p.quantity + int(q)
    Product.objects.filter(bname=b,name=pn,size=ps).update(quantity=uq)
    Purchase.objects.create(pp=p,prate=r,pquantity=q,pnotes=n)
    cp = int(q) * int(r)
    return render(request,'purchase_receipt.html', {'b':p.bname.bname,'pn':p.name,'ps':ps,'q':q,'r':r,'cp':cp,'n':n})

def purchase_history(request):
    p = Purchase.objects.all()
    return render(request, 'purchase_history.html', {'allpurchase': p})


def sale_form(request):
    b = Brand.objects.all()
    return render(request, 'sale.html', {'brands': b})

def sale(request):
    b = Brand.objects.get(bname=request.POST['brand_name'])
    pn = request.POST['product_name']
    ps = request.POST['product_size']
    p = Product.objects.get(bname=b,name=pn,size=ps)
    tc = request.POST['to_customer']
    r = request.POST['rate']
    q = request.POST['quantity']
    dt = request.POST['discount_type']
    d = request.POST['discount']
    if p.quantity >= int(q):
        if dt == 'none' or dt == 'flat':
            uq = p.quantity - int(q)
            sell_price = float(r) * int(q)
            discounted_sell_price = sell_price - float(d)
            Product.objects.filter(bname=b,name=pn,size=ps).update(quantity=uq)
            Sale.objects.create(sp=p,to_customer=tc,srate=r,squantity=q,discounttype=dt,discount=d,sprice=discounted_sell_price)
            return render(request,'sale_receipt.html', {'cn':tc,'b':p.bname.bname,'pn':pn,'ps':ps,'q':q,'r':r,'sp':discounted_sell_price})
        elif dt == 'percent':
            if float(d) > 0 and float(d) < 100:
                uq = p.quantity - int(q)
                sell_price = float(r) * int(q)
                pd = (float(d)/100) * sell_price
                discounted_sell_price = sell_price - pd
                Product.objects.filter(bname=b,name=pn,size=ps).update(quantity=uq)
                Sale.objects.create(sp=p,to_customer=tc,srate=r,squantity=q,discounttype=dt,discount=d,sprice=discounted_sell_price)
                return render(request,'sale_receipt.html', {'cn':tc,'b':p.bname.bname,'pn':pn,'ps':ps,'q':q,'r':r,'sp':discounted_sell_price})
            else:
                return HttpResponse("sell transaction failed - invalid percentage")
    else:
        return HttpResponse("no stock - please purchase")

def sale_history(request):
    s = Sale.objects.all()
    return render(request, 'sale_history.html', {'allsale': s})


def credit_form(request):
    return render(request, 'credit.html')

def credit(request):
    cn = request.POST['customer_name']
    ca = request.POST['credit_amount']
    Credit.objects.create(ccustomer=cn,camount=ca)
    return HttpResponse("credit added")

def credit_history(request):
    c = Credit.objects.all()
    return render(request, 'credit_history.html', {'allcredit': c})
