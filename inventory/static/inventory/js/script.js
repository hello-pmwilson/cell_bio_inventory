$(document).ready(function () {
	rows = $('section').slice(2) //excludes the title and form rows

	//change background color when a user hovers over a row
	$(rows).hover(
		function () {
			var id = $(this).attr('id');
			var children = this.children;
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

				var query = `/inventory/delete?selected=${window.selected}&delete=${id}`;
				$.ajax({
					url: query,
					type: 'GET',
					dataType: 'html',
					success: function () {
						console.log('success');
						//add logic to remove lines when deleted, then fix if delete was unsuccessful 
					},
					error: function (error) {
						console.error('Error fetching new content:', error);
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