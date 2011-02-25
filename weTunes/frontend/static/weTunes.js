
var last_updated = new Date();
var header_data = false;

// refresh the status of the player
function header_ajax()
{
  $.ajax({
    url:"/ajax/mpd_status",
  dataType: 'json',
  success: header_update
  });
}

// handle the player status response
function header_update(data)
{
  header_data = data;
  last_updated = new Date();
  currentsong_update();
}

// automatically adjust timing in header for elapsed time
function adjust_header_data()
{
  if (!header_data)
  {
    header_ajax();
    return;
  }
  var now = new Date();
  var delta = now.getUTCSeconds() - last_updated.getUTCSeconds();
  if (delta == 0) return;
  if (header_data["state"] == "play") {
    header_data["elapsed"] = parseInt(header_data["elapsed"]) + delta;
    if (header_data["elapsed"] >= header_data["cursong"]["time"]) {
      header_ajax();
      return;
    }
  }
  last_updated = now;
  currentsong_update();
}

// display the player status in the header
function currentsong_update()
{
  if (!header_data)
  {
    header_ajax();
    return;
  }

  //////////////////////////////////////
  // volume slider
  //////////////////////////////////////
  if ($("#volumeslider").slider("option", "value") != parseInt(header_data["volume"])) {
    $("#volumeslider").slider("option", "value", header_data["volume"]);
  }

  //////////////////////////////////////
  // control buttons
  //////////////////////////////////////
  var icon = header_data["state"] == "play" ? "ui-icon-wetunes-pause" : "ui-icon-wetunes-play";
  $("#playpausebutton").button({
    text:false,
    icons: {
      primary: icon
    },
  });

  //////////////////////////////////////
  // now playing
  //////////////////////////////////////
  $("#npprogressbar").progressbar("option", "value", 100*(header_data["elapsed"]/header_data["cursong"]["time"]));
  var d = new Date(header_data["elapsed"]*1000);
  $("#nptime").html(d.getUTCMinutes() + ":" + String('00'+d.getUTCSeconds()).slice(-2));
  d = new Date(header_data["cursong"]["time"]*1000);
  $("#nptotal").html(d.getUTCMinutes() + ":" + String('00'+d.getUTCSeconds()).slice(-2));
  // TODO: truncate title and artist if needed
  $("#nptitle").html(header_data["cursong"]["title"]);
  $("#npartist").html(header_data["cursong"]["artist"]);

}

//////////////////////////////////////
// initialize stuff at page load
//////////////////////////////////////
$(document).ready(function(){

//////////////////////////////////////
// search form
//////////////////////////////////////
$("#searchbox input[name=searchterm]").focusin(function(){
  if ($(this).val() == "Search") {
    $(this).val("");
  }
}).focusout(function(){
  if ($(this).val() == "") {
    $(this).val("Search");
  }
});

//////////////////////////////////////
// now playing progress bar
//////////////////////////////////////
$("#npprogressbar").progressbar({'value':0});


//////////////////////////////////////
// control buttons
//////////////////////////////////////
$("#playpausebutton").button({text: false, icons:{primary:'ui-icon-wetunes-play'}})
.click(function(){
  $.ajax({
    url:"/control/playpause",
    success: header_ajax
  });
});

$("#nextbutton").button({text: false, icons:{primary:'ui-icon-wetunes-next'}})
.click(function(){
  $.ajax({
    url:"/control/next",
    success: header_ajax
  });
});

//////////////////////////////////////
// volume slider
//////////////////////////////////////
$("#volumeslider").slider({ orientation: 'vertical',
  max: 100,
  min: 0,
  stop: function(event, ui) { $.ajax({url:"/control/setvolume/"+ui.value});}
});

// set timers to do constant player updates
// TODO: maybe use a comet call instead

// refresh from server every 15 seconds
var t = setInterval("header_ajax()", 15000);
// refresh the ui based on elapsed time every second
// (automatically updates from server if the song is over)
var u = setInterval("adjust_header_data()", 1000);
header_ajax();
    
}); // document ready

// vim: ft=javascript sw=2 ts=2 et
