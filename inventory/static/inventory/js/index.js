$(document).ready(function() {
  var dataDiv = $("#data")
  var defaultURL = dataDiv.attr("defaultURL")
  //When the page is called, make the API call for the data to load in
  $.ajax({
    url: defaultURL,
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
      }

  loopLoadingFlask();
  var loopLoadingFlask = setInterval(loopLoadingFlask,500);
  setTimeout(function() {
      clearInterval(loopLoadingFlask); // This will stop the interval after 5 seconds
    }, 5000);

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
              console.log(queryURL)
              var data = $(response);
              $("#data").html(data);
          },
          error: function(error) {
              console.error('Error fetching new content:', error);
          }
      });

  })


})
