$(document).ready(function() {
  rows = $('section').slice(2) //excludes the title and form rows

  //change background color when a user hovers over a row
  $(rows).hover(
    function() {
      const children = this.children;
      for (let i =0; i<children.length; i++) {
        $(children[i]).addClass('row-hover');
      }
    },
    function() {
      const children = this.children;
      for (let i =0; i<children.length; i++) {
        $(children[i]).removeClass('row-hover');
      }            
    }

  );

  //as user types in the search bar, search through all cells in the table
  //skipping the form row, and update what is shown in the table based on matches
  //case insensitive
  $('#search').keyup(function(e) {
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
  $(".bi-caret-down-fill").click(function(e) {
    var button = e.target;
    var buttonRect = button.getBoundingClientRect();
    var dropDown = e.target.nextElementSibling; //Works because the dropdown is the next sibling, fix in future if adding anything
    dropDown.style.left = buttonRect.right + 'px';
    dropDown.style.top = buttonRect.bottom + 'px';
    $(dropDown).toggle();

    var dropHover = false;
    $(button).mouseleave(function() {
      setTimeout(function() {
        if (!dropHover) {
          $(dropDown).hide();
        }
      }, 100); //give a milisecond to get to the drop down
    });
    $(dropDown).mouseenter(function() {
      dropHover = true;
    })
    $(dropDown).mouseleave(function() {
      $(dropDown).hide();
    })
  });

  $('.drop-down').find('i').click(function(e) {
    let orderBy = $(e.target).attr("order-by");
    var query = `/inventory/get_data?selected=${window.selected}&order_by=${orderBy}`;

    //send the query
    $.ajax({
    url: query,
    type: 'GET',
    dataType: 'html',
    success: function(response) {
        var data = $(response);
        $("#data").html(data);
    },
    error: function(error) {
        console.error('Error fetching new content:', error);
    }
    });
  });

    // 
    // //set query

  // var query = 
  
    
  // });

  // //when a caret is clicked, send a get request with the information
  // //and update the table with the new order W/O refreshing the whole page
  // //and toggle the orderID between ascending and descending
  // $(".bi-caret-down-fill").click(function(e) {
  //   console.log("clicky");
  //     let orderID = e.target.id

  //     //grab url for get request and edit url to be sent accordingly
  //     let url = window.location.href;
  //     if (url.includes('?')) { //if another parameter is already set
  //       var queryURL = window.location.href + `&order_by=${orderID}`;
  //     } else {
  //       var queryURL = window.location.href + `?order_by=${orderID}`;
  //     }

  //     //send get request and extract only the html we want to update
  //     $.ajax({
  //       url: queryURL,
  //       type: 'GET',
  //       dataType: 'html',
  //       success: function(response) {
  //         var db = $(response).find('tbody').html();
  //         $('tbody').html(db); //update the content with the reordered db
  //         onTableLoad();
  //       },
  //       error: function(error) {
  //         console.error('Error fetching new content:', error);
  //       }
  //     });

  //     toggleOrder(orderID); 
  // })

  // onTableLoad(); //set event listeners for items in the table

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
