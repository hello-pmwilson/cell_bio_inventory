$(document).ready(function () {
	rows = $('section').slice(2) //excludes the title and form rows

	//change background color when a user hovers over a row
	$(rows).hover(
		function () {
			var row = this
			var id = $(row).attr('id');
			var children = row.children;
			for (let i = 0; i < children.length; i++) {
				$(children[i]).addClass('row-hover');
			}
			var editOptions = $(children).find('.edit');
			$(editOptions).show();
			var deleteButton = $(editOptions).find('.delete');
			$(deleteButton).click(function () {
				if (id == 1 && (window.selected == 'unit' || window.selected == 'location')) {
					alert('Sorry, This value is set as the default. You cannot delete it.');
					return;
				};
				if (window.selected == 'add_item') {
					var userConfirm = confirm('Wait! Deleting an item from this database will delete all records with this item across all databases.\nDo you still want to delete?');
					if (!userConfirm) {
						return; //if user hits cancel, exit the function and do not delete
					}
				}

				//the deleted row will dissapear
				for (let i = 0; i < children.length; i++) {
					$(children[i]).toggle();
				}

				var query = `/inventory/delete?selected=${window.selected}&delete=${id}`;
				$.ajax({
					url: query,
					type: 'GET',
					dataType: 'html',
					success: function () {
						//if successful the row stays hidden 
					},
					error: function (error) {
						//if the deletion query fails the row will reappear and be red 
						console.error('Error fetching new content:', error);
						for (let i = 0; i < children.length; i++) {
							$(children[i]).toggle();
							$(children[i]).css('background-color', 'var(--fail)')
						};
						//for half a second before returning to normal
						setTimeout(function(){
							for (let i = 0; i < children.length; i++) {
								$(children[i]).css('background-color', '');
							};							
						}, 500)					
					}
				});
			})
		},
		function () {
			const children = this.children;
			for (let i = 0; i < children.length; i++) {
				$(children[i]).removeClass('row-hover');
			}
			var editOptions = $(children).find('.edit');
			$(editOptions).hide();
			var deleteButton = $(editOptions).find('.delete');
			$(deleteButton).off();
		}

	);

	var cells = $(rows).find("div");


	$('.edit-record').click(function(e) {
		var section = $($($(e.target).parent()).parent()).parent();
		var sectionID = $(section).attr('id')

		if (sectionID == 1 && (window.selected == 'unit' || window.selected == 'location' || window.selected == 'add_item')) {
			alert('Sorry, This value is set as the default. You cannot change it.');
			return;
		};

		var sectionChildren = $(section).children()
		var originalValues = {}
		sectionChildren.each(function(index, element){
			let elementClass = $(element).attr('class').split(' ')[0];
			let elementValue = $(element).text();
			originalValues[elementClass] = elementValue;		
		})

	// Create the modal popup dynamically using jQuery
	var modal = $('<div>', {
		class: 'modal',
		id: 'myModal'
	});

	var modalContent = $('<div>', {
		class: 'modal-content'
	});

	var closeBtn = $('<span>', {
		class: 'close',
		html: '&times;',

	});

	var formContent = $('#form').html()
	var formContentObj = $($.parseHTML(formContent));
	formSection = formContentObj.find('section')
	formItems = formSection.children()
	$(formItems).each(function(index, element){
		var elementClass = $(element).attr('class').trim();
		var elementValue = originalValues[elementClass];
		var formChild = $(element).children()[0] 
		var formChildTag = $(formChild).prop('tagName')
		if (formChildTag == 'INPUT') {
			if ($(formChild).prop('id') == 'submit') {
				//pass
			} else {
			$(formChild).attr('value', elementValue);
			}
		} else if (formChildTag == 'SELECT') {
			var options = $(formChild).find('option')
			options.removeAttr('selected');
			var op = $(options).filter(function(){
        return $(this).html() === elementValue;
    });
			$(op).attr('selected','selected');
		} else if  (formChildTag == 'TEXTAREA') {
			$(formChild).text(elementValue);
		} else {
			//pass
		}
		
		
	})
	var formHTML = $(formContentObj[1])[0].outerHTML;

	var content = $('<p>', {
		html: formHTML
	});

	// Append elements to modalContent
	modalContent.append(closeBtn, content);

	// Append modalContent to modal
	modal.append(modalContent);

	// Append modal to body
	$('body').append(modal);	
	
	$('.close').click(function(){
		$("#myModal").remove();
	})

	var submitBtn = $('#myModal').find('#submit')
	$(submitBtn).click(function(e){
		e.preventDefault();
		const formData = $('#myModal').find('form');
		var qurl = `/inventory/edit?id=${sectionID}`
		$.ajax({
			url: qurl,
			type: 'POST',
			data: formData.serialize(),
			dataType: 'json',
			success: function(data) {
					if (data.status === 'success') {
							$("#myModal").remove();
							reload();
					} else {
							alert('Error occurred');
					}
			},
			error: function(error) {
					console.error('Error:', error);
					alert('Error occurred');
			}
	});			


	})
});


  $('form').submit(function(e){
		e.preventDefault();
		const formData = $('form').serialize();
    $.ajax({
			url: $('form').attr('action'),
			type: 'POST',
			data: formData,
			dataType: 'json',
			success: function(data) {
					if (data.status === 'success') {
							reload_add();
					} else {
							alert('Error occurred');
					}
			},
			error: function(error) {
					console.error('Error:', error);
					alert('Error occurred');
			}
	});		
	})

//when django sends a request to reload after adding a new record
function reload_add() {
	selected = window.selected;
	orderBy = '-id';
	query = `/inventory/get_data?selected=${window.selected}&order_by=${orderBy}`;
	$.ajax({
		url: query,
		type: 'GET',
		dataType: 'html',
		success: function (response) {
			var data = $(response);
			$("#data").html(data);
		},
		error: function (error) {
			console.error('Error fetching new content:', error);
		}
	});
}

function reload(){
	selected = window.selected;
	query = `/inventory/get_data?selected=${window.selected}`;
	$.ajax({
		url: query,
		type: 'GET',
		dataType: 'html',
		success: function (response) {
			var data = $(response);
			$("#data").html(data);
		},
		error: function (error) {
			console.error('Error fetching new content:', error);
		}
	});
};


	//as user types in the search bar, search through all cells in the table
	//skipping the form row, and update what is shown in the table based on matches
	//case insensitive
	$('#search').keyup(function (e) {
		var search = e.target.value.toLowerCase();
		for (let i = 0; i < $(rows).length; i++) {
			text = $(rows[i]).text().toLowerCase()
			let showRow = text.indexOf(search) !== -1 ? "" : "none";
			$(rows[i]).css('display', showRow);
		}
	})

	//When a caret is clicked, a drop down menu appears
	//The drop down will hide if the mouse leaves the button without entering the drop down or once leaving the drop down
	//clicking on an option in the dropdown will send a request to reorder the data based on the selected option
	$(".bi-caret-down-fill").click(function (e) {
		var button = e.target;
		var buttonRect = button.getBoundingClientRect();
		var dropDown = e.target.nextElementSibling; //Works because the dropdown is the next sibling, fix in future if adding anything
		dropDown.style.left = buttonRect.right + 'px';
		dropDown.style.top = buttonRect.bottom + 'px';
		$(dropDown).toggle();

		var dropHover = false;
		$(button).mouseleave(function () {
			setTimeout(function () {
				if (!dropHover) {
					$(dropDown).hide();
				}
			}, 100); //give a milisecond to get to the drop down
		});
		$(dropDown).mouseenter(function () {
			dropHover = true;
		})
		$(dropDown).mouseleave(function () {
			$(dropDown).hide();
		})
	});

	$('.drop-down').find('i').click(function (e) {
		let orderBy = $(e.target).attr("order-by");
		var query = `/inventory/get_data?selected=${window.selected}&order_by=${orderBy}`;

		//send the query
		$.ajax({
			url: query,
			type: 'GET',
			dataType: 'html',
			success: function (response) {
				var data = $(response);
				$("#data").html(data);
			},
			error: function (error) {
				console.error('Error fetching new content:', error);
			}
		});
	});

})