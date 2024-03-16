##currently working on
#add methods for adding and deleting lines
#add code for implementing those methods

from django.shortcuts import render
from django.template.loader import render_to_string
from .forms import onRequestForm, inventoryAddForm, itemAddForm, unitForm, locationForm
from .models import inventory, on_request, item, unit, location
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

	def query(self, *args):
		#call for the data to fill the template
		#include any number of order by parameters
		q = self.db.objects.all()
		if args:
			q = q.order_by(*args)
		return q

	def render_data(self, request, order_by='id'):
		csrf_token = get_token(request)
		context = {
			'defaultURL': self.url,
			'form': self.form,
			'data': self.query(order_by),
			'itemList': item.objects.all(),
			'csrf_token': csrf_token
		}
		return render_to_string(self.url, context)

	def delete(self, delete_id):
		record = self.db.objects.get(pk=delete_id)
		print('would delete' , record)
		# record.delete()

    
inv = data('inventory', inventoryAddForm, inventory, 'inventory/inventory.html')
req = data('requests', onRequestForm, on_request, 'inventory/requests.html')
a_item = data('add item', itemAddForm, item, 'inventory/add_item.html')
loc = data('locations', locationForm, location, 'inventory/location.html')
un = data('units', unitForm, unit, 'inventory/unit.html')

data_dict = {
	'inventory': inv,
	'requests': req,
	'add_item': a_item,
	'location': loc,
	'unit': un
}

#main view when calling url/inventory
#loads different defaults based on selected link
#update the defaults with the selected section including the forms, the databases, the order_by, and the query

@login_required
@csrf_protect
def index(request):  
	return render(request, 'inventory/index.html')

def get_data(request):
	if 'selected' in request.GET:
		selected = request.GET['selected']
	else:
		selected = 'inventory' #set the default
	if 'order_by' in request.GET:
		order_by = request.GET['order_by']
		return HttpResponse(data_dict[selected].render_data(request, order_by=order_by))
	return HttpResponse(data_dict[selected].render_data(request))

def delete(request):
	print(request)
	delete_id = request.GET['delete']
	selected = request.GET['selected']
	print(delete_id)
	print(selected)
	data_dict[selected].delete(delete_id)
	return HttpResponse(status=204)

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