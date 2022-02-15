from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render , redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pyrebase
import datetime
config={
  "apiKey": "AIzaSyC_XKRXz-MqitjSwHyOf1r04RqX9KTaaQY",
  "authDomain": "test-29619.firebaseapp.com",
  "databaseURL": "https://test-29619-default-rtdb.firebaseio.com",
  "projectId": "test-29619",
  "storageBucket": "test-29619.appspot.com",
  "messagingSenderId": "266450549582",
  "appId": "1:266450549582:web:51b2605ba63f6d58fefc1f",
  "measurementId": "G-VJNQYNFH4V"
}
firebase=pyrebase.initialize_app(config)
db=firebase.database()

config2 = {
  "apiKey": "AIzaSyB5CQ7Bvog4rV-k0b5rI5Tn_lTFf0iaYe8",
  "authDomain": "rounds-b9463.firebaseapp.com",
  "databaseURL": "https://rounds-b9463-default-rtdb.firebaseio.com/",
  "projectId": "rounds-b9463",
  "storageBucket": "rounds-b9463.appspot.com",
  "messagingSenderId": "553782809817",
  "appId": "1:553782809817:web:d84698a4f5dd3e79f81ac8",
  "measurementId": "G-MHE7P5FMW5"
};
firebase2=pyrebase.initialize_app(config2)
db2=firebase2.database()
def show(request):
    return render(request, 'analytics/show.html')




@csrf_exempt
def crud(request):
    if request.method=="POST":
        db2.child("Row").push({"category":request.POST.get('category'),"city":request.POST.get('city'),"company":request.POST.get('company'),"fundedDate":request.POST.get('fundedDate'),"numEmps":request.POST.get('numEmps'),"permalink":request.POST.get('permalink'),"raisedAmt":request.POST.get('raisedAmt'),"raisedCurrency":request.POST.get('raisedCurrency'),"round":request.POST.get('round'),"state":request.POST.get('state')})
        if request.POST.get('permalink') not in db.get().val():
            db.child(request.POST.get('permalink')).child("Details").set({"category":request.POST.get('category'),"city":request.POST.get('city'),"company":request.POST.get('company'),"numEmps":request.POST.get('numEmps'),"state":request.POST.get('state')})
            db.child(request.POST.get('permalink')).child("Funding_Trades").child(0).set({"fundedDate":request.POST.get('fundedDate'),"raisedAmt":request.POST.get('raisedAmt'),"raisedCurrency":request.POST.get('raisedCurrency'),"round":request.POST.get('round')})
            db.child(request.POST.get('permalink')).child("Total_Funds").set(request.POST.get('raisedAmt'))
        else:
            trades=db.child(request.POST.get('permalink')).child("Funding_Trades").get()
            nextidx=len(trades.each())
            db.child(request.POST.get('permalink')).child("Funding_Trades").child(nextidx).set({"fundedDate":request.POST.get('fundedDate'),"raisedAmt":request.POST.get('raisedAmt'),"raisedCurrency":request.POST.get('raisedCurrency'),"round":request.POST.get('round')})
            oldTF=db.child(request.POST.get('permalink')).child("Total_Funds").get().val()
            nF=int(request.POST.get('raisedAmt'))
            nTf=int(oldTF)+nF
            db.child(request.POST.get('permalink')).update({"Total_Funds":nTf})
    return render(request,'pages/crud.html')






def companylistapi(request):
    alldata=db.get()
    cList=[]
    for comp in alldata.each():
        plink=comp.key()
        cList.append(plink)
        rnds=['a','b','c','d','e','seed','angel','debt_round']
    context={'cList':cList,'rnds':rnds}
    return render(request,'pages/index.html',context)


def round(request,pl):
    d=db2.child("Row").order_by_child("round").equal_to(pl).get().val()
    context={'d':d,'pl':pl}
    return render(request,'pages/round.html',context)

def company(request,pl):
    d=db.child(pl).get().val()
    trades=db.child(pl).child('Funding_Trades').get().val()
    context={'d':d,'pl':pl}
    return render(request,'pages/company.html',context)

def companybarapi(request,pl):
    d=db.child(pl).child('Funding_Trades').get().val()
    ans=[]
    for k in d:
        dii = {}
        y=k['fundedDate'][-2:]
        m=k['fundedDate'][3:6]
        d=k['fundedDate'][:2]
        do=datetime.datetime.strptime(m,"%b")
        mn=do.month
        if mn<10:
            mnstr='0'+str(mn)
        else:
            mnstr=str(mn)
        if 25<int(y)<=99:
            y='19'+y
        else:
            y='20'+y
        fdate=y+'-'+mnstr+'-'+d
        dii['x']=fdate
        dii['y']=k['raisedAmt']
        ans.append((dii))
    return JsonResponse(ans,safe=False)

def state(request):
    return render(request, 'analytics/statewise.html')

def category(request):
    return render(request, 'analytics/categorywise.html')


def statewise(request):
    alldata=db.get()
    std={}
    for comp in alldata.each():
        state=comp.val()['Details']['state']
        tf=comp.val()['Total_Funds']
        if state not in std:
            std[state]=tf
        else:
            ct=std[state]
            std[state]=ct+tf
    
    return JsonResponse(std,safe=False)

def categorywise(request):
    alldata=db.get()
    std={}
    for comp in alldata.each():
        state=comp.val()['Details']['category']
        tf=comp.val()['Total_Funds']
        if state not in std:
            std[state]=tf
        else:
            ct=std[state]
            std[state]=ct+tf
    
    return JsonResponse(std,safe=False)