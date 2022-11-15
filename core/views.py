from django.shortcuts import render

# Create your views here.
import requests
import os
import json

def currency_data():
    module_dir=os.path.dirname(__file__)
    
    file_path=os.path.join(module_dir,'currencies.json')
    with open(file_path,'r') as f:
        currency_data=json.loads(f.read())

    return currency_data

def index(request):
    if request.method=='POST':
        amount=float(request.POST.get('amount'))
        currency_from=request.POST.get('currency_from')
        currency_to=request.POST.get('currency_to')

        url=f"https://open.er-api.com/v6/latest/{currency_from}"
        d=requests.get(url).json()

        if d['result']=='success':
            ex_target=d['rates'][currency_to]
            result=ex_target*amount
            result="{:.2f}".format(result)
            context={
                'result':result,
                'currency_to':currency_to,
                'currency_data':currency_data
            }
            return render(request,'index.html',context=context)
    return render(request,'index.html',{'currency_data':currency_data()})
