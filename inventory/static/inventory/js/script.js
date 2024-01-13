console.log("hello world");
$(document).ready(function() {
    //when a caret is clicked, send a get request with the information
    //and update the table with the new order W/O refreshing the whole page
    //and toggle the orderID between ascending and descending
    $(".bi-caret-down-fill").click(function(e) {
        let orderID = e.target.id

        //grab url for get request and edit url to be sent accordingly
        let url = window.location.href;
        if (url.includes('?')) { //if another parameter is already set
            var queryURL = window.location.href + `&order_by=${orderID}`;
        } else {
            var queryURL = window.location.href + `?order_by=${orderID}`;
        }

        //send get request and extract only the html we want to update
        $.ajax({
            url: queryURL,
            type: 'GET',
            dataType: 'html',
            success: function(response) {
                var db = $(response).find('tbody').html();
                $('tbody').html(db); //update the content with the reordered db
            },
            error: function(error) {
                console.error('Error fetching new content:', error);
            }
        });

        toggleOrder(orderID); 
    })

    //as user types in the search bar, search through all cells in the table
    //skipping the form row, and update what is shown in the table based on matches
    //case insensitive
    $('#search').keyup(function(e) {
        var filter = e.target.value.toLowerCase();
        var rows = $('tbody').find('tr:not(:first)');

        for (var i = 1; i < rows.length; i++) {
            var row = rows[i]
            var cells = row.getElementsByTagName('td');
            var showRow = false;

            for (var j = 0; j < cells.length; j++) {
                var cell = cells[j];
          
                if (cell.innerHTML.toLowerCase().indexOf(filter) > -1) {
                  showRow = true;
                  break;
                }
              }
          
              row.style.display = showRow ? "" : "none";
        }
    })

    //when hovering over a row, the option to delete should appear
    const rows = $('tbody').find('tr:not(:first)');
    rows.on({
    mouseenter: function () {
        $(this).find('.delete').css('visibility', 'visible');
      },
      mouseleave: function () {
        $(this).find('.delete').css('visibility', 'hidden' );
      }
    });

    
    //delete a record from the db
    $('.delete').click(function(e) {
        let id = e.target.id;
        url = getQueryURL() + `delete=${id}`;

        if (url.includes('add_item')) {
            var userConfirm = confirm('Wait! Deleting an item from this database will delete all records with this item across all databases.\nDo you still want to delete?');
            if (!userConfirm) {
                return; //if user hit cancels, exit the function and do not delete
            }
        }
        

        $.ajax({
            url: url,
            type: 'GET',
            success: function() {
                var row = findRow(id.toString());
                row.style.display = 'none';
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    })

})

//given an orderID, switch between ascending and descending
function toggleOrder(orderID) {
    let toggle = orderID.slice(); //copy the string to be toggled
    //toggle it
    if (toggle.startsWith('-')) {
        toggle = toggle.substring(1);
    } else {
        toggle = '-' + toggle
    }
    //set the orderID to the new toggled string
    $(`#${orderID}`).attr('id', toggle);
}

//grab url for get request and edit url to be sent accordingly
function getQueryURL() {    
    let url = window.location.href;
    if (url.includes('?')) { //if another parameter is already set
        return window.location.href + '&';
    } else {
        return window.location.href + '?';
    }
}

function findRow(id) {
    var rows = $('tbody').find('tr:not(:first)'); //grab all the rows excluding the form
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i]
        var cell = row.getElementsByTagName('td'); //grab the id, then check if it matches the provided id
        if (cell[0].innerHTML.toString() == id) {
            return row;   
        }
    }
}