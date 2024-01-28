from django.shortcuts import render, redirect
from .forms import onRequestForm, inventoryAddForm, itemAddForm, unitForm, locationForm
from .models import inventory, on_request, item, unit, location, category
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

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
        if type(form) is list:
            for possiblySubmittedForm in form:
                if possiblySubmittedForm.is_valid():
                        possiblySubmittedForm.save()
                        return redirect(request.get_full_path())
        if 'item_char' in request.POST:
            request.POST = request.POST.copy()
            check_item = request.POST['item_char']
            request.POST.pop('item_char', None)
            query, created = item.objects.get_or_create(item=check_item, defaults={'item_description':'TBD', 'category': category.objects.get(pk=1)})
            request.POST['item'] = item.objects.get(item=query).id
        if selected == 'inventory':
            form = inventoryAddForm(request.POST)
        elif selected == 'requests':
            form = onRequestForm(request.POST)
             
        if form.is_valid():
            form.save()
            return redirect(request.get_full_path())
        else:
            print(form.errors)
    
    #if delete is selected on a record, delete the record
    if 'delete' in request.GET:
        delete = request.GET['delete'].split(',')
        id = delete[0]
        if delete[1] == 'units':
            db = unit
        elif delete[1] == 'locations':
            db = location
        record = db.objects.get(pk=id)
        record.delete()

    #save finalized values and render page
    context = {
        'defaultURL': defaultURL,
        'form': form,
        'data': q,
        'itemList': item.objects.all()
    }

    return render(request, 'inventory/index.html', context)