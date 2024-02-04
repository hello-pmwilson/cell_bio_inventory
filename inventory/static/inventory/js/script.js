$(document).ready(function() {
    // var itemFormField = $('#item_char_field');
    // if (itemFormField) {
    //     itemFormField.list = 'itemOptions';
    //     console.log("this bit happened")
    // };

    
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
                onTableLoad();
            },
            error: function(error) {
                console.error('Error fetching new content:', error);
            }
        });

        toggleOrder(orderID); 
    })

    onTableLoad(); //set event listeners for items in the table



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

//when the table is loaded or reloaded after page refresh/ajax/etc
//call functions that set event listeners for the table
function onTableLoad() {
    setRowHover();
    setDeleteButtons();
}

function setRowHover() {
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
}

function setDeleteButtons() {
        //delete a record from the db
        $('.delete').click(function(e) {
            let id = e.target.closest('tr').id; //the id of the element to delete from the db
            let formID = e.target.closest('form').id; //the db to delete it from
            let row = e.target.closest('tr'); //the row which will be removed from the page upon deletion

            url = getQueryURL() + `delete=${id},${formID}`;
    
            if (url.includes('add_item')) {
                var userConfirm = confirm('Wait! Deleting an item from this database will delete all records with this item across all databases.\nDo you still want to delete?');
                if (!userConfirm) {
                    return; //if user hit cancels, exit the function and do not delete
                }
            }

            if (url.includes('=1,units') || url.includes('=1,location')) {
                alert('Sorry, This value is set as the default. You cannot delete it.');
                return
            }
            
    
            $.ajax({
                url: url,
                type: 'GET',
                success: function() {
                    row.style.display = "none";
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        })
}
