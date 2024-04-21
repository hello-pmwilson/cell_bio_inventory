##currently working on
#add methods for adding and deleting lines
#add code for implementing those methods

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .forms import onRequestForm, inventoryAddForm, itemAddForm, unitForm, locationForm
from .models import inventory, on_request, item, unit, location, category
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from django.middleware.csrf import get_token

from time import sleep

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
		record.delete()
	
	def add(self, request):
		if self.form(request).is_valid():
			self.form(request).save() 
		else:
			print(self.form(request).errors)

	def edit(self, request, edit_id):
		print("method edit reached")
		record = self.db.objects.get(pk=edit_id)
		form = self.form(request, instance=record)
		if form.is_valid():
			print("for save success")
			form.save()
		

    
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
	delete_id = request.GET['delete']
	selected = request.GET['selected']
	data_dict[selected].delete(delete_id)
	return HttpResponse(status=204)
	# return HttpResponseServerError('Simulation')

def add(request):
	#check the selected item. If blank use a default. If the form is the add_item form, add the item. 
	#if not check if the selected item exists and create it if it doesnt.
	if request.method == "POST":
		request.POST = request.POST.copy()
		selected = request.POST['form_is']
		if 'item_char' in request.POST:
			selected_item = request.POST.pop('item_char', None)[0].strip()
			if selected_item == '':
				selected_item = item.objects.get(item='Lab Stuff')
			else:
				if selected == 'add_item': 
					request.POST['item'] = selected_item
					a_item.add(request.POST)
				else:	
					item_query, created = item.objects.get_or_create(item=selected_item, defaults={'item_description':'TBD', 'category': category.objects.get(pk=1)})
					request.POST['item'] = item.objects.get(item=item_query).id
		data_dict[selected].add(request.POST)

	return JsonResponse({'status': 'success', 'message': 'Form submitted successfully'})

def edit(request):
	print("edit reached")
	request.POST = request.POST.copy()
	selected = request.POST['form_is']	
	qinstance = request.GET['id']
	if 'item_char' in request.POST:
		selected_item = request.POST.pop('item_char', None)[0].strip()
	if selected_item == '':
		item_query = item.objects.get(item=inventory.objects.get(pk=qinstance))
	else: 
		if selected == 'add_item': 
			request.POST['item'] = selected_item
			print('post' , request.POST['item'])
			a_item.edit(request.POST, qinstance)
			return JsonResponse({'status': 'success', 'message': 'Form submitted successfully'})
		item_query, created = item.objects.get_or_create(item=selected_item, defaults={'item_description':'TBD', 'category': category.objects.get(pk=1)})
	request.POST['item'] = item.objects.get(item=item_query).id
	print("request" , request.POST['item'])
	data_dict[selected].edit(request.POST, qinstance)
	return JsonResponse({'status': 'success', 'message': 'Form submitted successfully'})


def skeleton(request):
  return render(request, 'inventory/skeleton.html')