$(document).ready(function() {
    //Loading Animation - Loading Flask
    //Thanks yqnn.github.io/svg-path-editor/ for the editor which was used to make the svg
    var loadingFlaskPath = $("#loading-flask-path")
    const paths = [
        "m8 53q-10 0-1-12l6-6v-18q-5-4 0-4h7q5 0 0 4v18l6 6q10 12 0 12h-18m6-39q-3 0 0 2v19l-6 6q5-3 11 1 4 2 6-1l-6-6v-19q3-2 0-2M15 5A1 1 0 0013 7 1 1 0 0015 5M21-2A1 1 0 0021 1 1 1 0 0021-2M15-13A1 1 0 0015-10 1 1 0 0015-13",
        "m8 53q-10 0-1-12l6-6v-18q-5-4 0-4h7q5 0 0 4v18l6 6q10 12 0 12h-18m6-39q-3 0 0 2v19l-6 6q1 5 9 1 6-2 8-1l-6-6v-19q3-2 0-2m2-8a1 1 0 002 2 1 1 0 00-2-2m-8-6a1 1 0 00-2 2 1 1 0 002-2m8-9a1 1 0 002 2 1 1 0 00-2-2"]
    var i = 0;
    function loopLoadingFlask() {
        var d = i % 2 === 0 ? 0 : 1;
        loadingFlaskPath.attr("d", paths[d]);
        i++;
        setTimeout(loopLoadingFlask, 500); // Wait half a second before calling the loop again
        }
    
    // loopLoadingFlask(); // Start the loop
    

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


    const tabColors = {
        "inventory": ["#aed9e0", "#93c8d3"], //blue
        "requests": ["#a0d9bf", "#90c8ab"], //green
        "addItem": ["#ffc0cb", "#ffb6c1"], //pink
        "settings": ["#9c8bb1", "#817f9b"] //purple
    }
    const inventoryTab = $("#inventory")
    const requestTab = $("#requests")
    const addItemTab = $("#addItem")
    const settingsTab = $("#settings")

    
    //when selecting new tabs, change the color of the page. get the color from the tabColors object
    var tabs = $(".tab")
    tabs.click(function(e) {
        //change the color
        var primaryColor = tabColors[e.target.id][0];
        var secondaryColor = tabColors[e.target.id][1];
        tabs.addClass("inactive");
        $(e.target).removeClass("inactive");
        $('html').css('--primary-color', primaryColor);
        $('html').css('--secondary-color', secondaryColor);
        //get the information to load
        let queryURL = this.getAttribute('href')

        //send get request and extract only the html we want to update
        $.ajax({
            url: queryURL,
            type: 'GET',
            dataType: 'html',
            success: function(response) {
                var data = $(response).find('#data-data').html();
                console.log(data);
                $("#data-data").html(data);
            },
            error: function(error) {
                console.error('Error fetching new content:', error);
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
                    return; //if user hits cancel, exit the function and do not delete
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
