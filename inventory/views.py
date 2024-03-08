##currently working on
##adding if states to index. change url to point to the index instead and then if get data in the get request call the function to render that information
#do this with other function as well. everything should be in the index but each thing will be a different function. 


from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .forms import onRequestForm, inventoryAddForm, itemAddForm, unitForm, locationForm
from .models import inventory, on_request, item, unit, location, category
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.middleware.csrf import get_token

class data:
	def __init__(self, title, form, db, url):
		self.title = title
		self.form = form
		self.db = db
		self.url = url

	def __str__(self):
		return f"{self.title}"

	def query(self, **kwargs):
		#call for the data to fill the template
		#include any number of order by parameters
		q = self.db.objects.all()
		if kwargs:
			q = q.order_by(*kwargs.values())
		return q

	def render_data(self, request):
		csrf_token = get_token(request)
		context = {
			'defaultURL': self.url,
			'form': self.form,
			'data': self.query(),
			'itemList': item.objects.all(),
			'csrf_token': csrf_token
		}
		return render_to_string(self.url, context)
    
inv = data('inventory', inventoryAddForm, inventory, 'inventory/inventory.html')
req = data('requests', onRequestForm, on_request, 'inventory/requests.html')
a_item = data('add item', itemAddForm, item, 'inventory/add_item.html')

data_dict = {
	'inventory': inv,
	'requests': req,
	'add_item': a_item
}

#main view when calling url/inventory
#loads different defaults based on selected link
#update the defaults with the selected section including the forms, the databases, the order_by, and the query

@login_required
@csrf_protect
def index(request):  
	if 'get_it' in request.GET:
		return inv.render_data()
	return render(request, 'inventory/index.html')

def get_data(request):
	if 'selected' in request.GET:
		selected = request.GET['selected']
	else:
		selected = 'inventory' #set the default
	return HttpResponse(data_dict[selected].render_data(request))

	# #check if specific template is called to load, and if not set default
	# if 'selected' in request.GET:
	# 		selected = request.GET['selected']
	# else:
	# 		selected = 'inventory' #set the default

	# #based on selected template, load data to fill in html
	# if selected == 'inventory':
	# 		form = inventoryAddForm(request.POST or None)
	# 		ordering = 'id'
	# 		db = inventory
	# 		q = db.objects.all().order_by(ordering)
	# 		defaultURL = 'inventory/inventory.html'
	# elif selected == 'requests':
	# 		form = onRequestForm(request.POST or None)
	# 		ordering = 'id'
	# 		db = on_request
	# 		q = db.objects.all().order_by(ordering)
	# 		defaultURL = 'inventory/requests.html'
	# elif selected == 'add_item':
	# 		form = itemAddForm(request.POST or None)
	# 		ordering = 'item'
	# 		db = item
	# 		q = db.objects.all().order_by(ordering)
	# 		defaultURL = 'inventory/add_item.html' 
	# elif selected == 'settings':
	# 	form = [unitForm(request.POST or None), locationForm(request.POST or None)]
	# 	q = [unit.objects.all(), location.objects.all()]
	# 	defaultURL = 'inventory/settings.html'  
	
	# #check if order_by is set and update the query accordingly
	# if 'order_by' in request.GET:
	# 	ordering = request.GET['order_by']
	# 	q = db.objects.all().order_by(ordering)
	
	# #if form submitted, check validity and save
	# if request.method == "POST":
	# 	if type(form) is list:
	# 		for possiblySubmittedForm in form:
	# 			if possiblySubmittedForm.is_valid():
	# 				possiblySubmittedForm.save()
	# 				return redirect(request.get_full_path())
	# 	if 'item_char' in request.POST:
	# 		request.POST = request.POST.copy()
	# 		check_item = request.POST['item_char']
	# 		request.POST.pop('item_char', None)
	# 		query, created = item.objects.get_or_create(item=check_item, defaults={'item_description':'TBD', 'category': category.objects.get(pk=1)})
	# 		request.POST['item'] = item.objects.get(item=query).id
	# 	if selected == 'inventory':
	# 		form = inventoryAddForm(request.POST)
	# 	elif selected == 'requests':
	# 		form = onRequestForm(request.POST)
					
	# 	if form.is_valid():
	# 		form.save()
	# 		return redirect(request.get_full_path())
	# 	else:
	# 		print(form.errors)
	
	# #if delete is selected on a record, delete the record
	# if 'delete' in request.GET:
	# 	if 'formInventory' in request.GET:
	# 		print("hidden widget") 
	# 	delete = request.GET['delete'].split(',')
	# 	id = delete[0]
	# 	if delete[1] == 'units':
	# 		db = unit
	# 	elif delete[1] == 'locations':
	# 		db = location
	# 	record = db.objects.get(pk=id)
	# 	record.delete()

	# #save finalized values and render page
	# context = {
	# 	'rendered_data': inv.render_data(),
	# 	# 'defaultURL': defaultURL,
	# 	# 'form': form,
	# 	# 'data': q,
	# 	# 'itemList': item.objects.all()
	# }
	# return HttpResponse(inv.render_data(request)) #render(request, defaultURL, context)

def skeleton(request):
  return render(request, 'inventory/skeleton.html')