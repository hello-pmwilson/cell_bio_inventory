from django.shortcuts import render, redirect
from .forms import onRequestForm, inventoryAddForm, itemAddForm, unitForm, locationForm
from .models import inventory, on_request, item, unit, location
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db import connection



#main view when calling url/inventory
#loads different defaults based on selected link
#update the defaults with the selected section including the forms, the databases, the order_by, and the query
@login_required
@csrf_protect
def index(request):
    #check if specific template is called to load, and if not set default
    if 'selected' in request.GET:
        selected = request.GET['selected']
    else:
        selected = 'inventory' #set the default

    #based on selected template, load data to fill in html
    if selected == 'inventory':
        form = inventoryAddForm(request.POST or None)
        ordering = 'id'
        db = inventory
        q = db.objects.all().order_by(ordering)
        defaultURL = 'inventory/inventory.html'
    elif selected == 'requests':
        form = onRequestForm(request.POST or None)
        ordering = 'id'
        db = on_request
        q = db.objects.all().order_by(ordering)
        defaultURL = 'inventory/requests.html'
    elif selected == 'add_item':
        form = itemAddForm(request.POST or None)
        ordering = 'item'
        db = item
        q = db.objects.all().order_by(ordering)
        defaultURL = 'inventory/add_item.html' 
    elif selected == 'settings':
        form = [unitForm(request.POST or None), locationForm(request.POST or None)]
        q = [unit.objects.all(), location.objects.all()]
        defaultURL = 'inventory/settings.html'  
    
    #check if order_by is set and update the query accordingly
    if 'order_by' in request.GET:
        ordering = request.GET['order_by']
        q = db.objects.all().order_by(ordering)
    
    #if form submitted, check validity and save
    if request.method == "POST":
        print(request.POST)

        if type(form) is list:
            for possiblySubmittedForm in form:
                print(form)
                if possiblySubmittedForm.is_valid():
                    print('valid')
                    possiblySubmittedForm.save()
                    return redirect(request.get_full_path())
        else:
            if form.is_valid():
                form.save()
                return redirect(request.get_full_path())
    
    #if delete is selected on a record, delete the record
    if 'delete' in request.GET:
        delete = request.GET['delete'].split(',')
        id = delete[0]
        if delete[1] == 'units':
            db = unit
        elif delete[1] == 'locations':
            db = location
        record = db.objects.get(pk=id)
        print("delete would've happened")
        record.delete()

    #save finalized values and render page
    context = {
        'defaultURL': defaultURL,
        'form': form,
        'data': q
    }

    return render(request, 'inventory/index.html', context)