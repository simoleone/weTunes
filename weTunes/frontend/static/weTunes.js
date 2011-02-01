function header_ajax()
{
  $.ajax({
    url:"/ajax/mpd_status",
  dataType: 'json',
  success: header_update
  });
}

function header_update(data)
{

  //////////////////////////////////////
  // volume slider
  //////////////////////////////////////
  $("#volumeslider").slider("option", "value", data["volume"]);

  //////////////////////////////////////
  // control buttons
  //////////////////////////////////////
  var icon = data["state"] == "play" ? "ui-icon-wetunes-pause" : "ui-icon-wetunes-play";
  $("#playpausebutton").button({
    text:false,
    icons: {
      primary: icon
    },
  });

  //////////////////////////////////////
  // now playing
  //////////////////////////////////////
  $("#npprogressbar").progressbar("option", "value", 100*(data["elapsed"]/data["cursong"]["time"]));
  var d = new Date(data["elapsed"]*1000);
  $("#nptime").html(d.getUTCMinutes() + ":" + String('00'+d.getUTCSeconds()).slice(-2));
  d = new Date(data["cursong"]["time"]*1000);
  $("#nptotal").html(d.getUTCMinutes() + ":" + String('00'+d.getUTCSeconds()).slice(-2));
  // TODO: truncate title and artist if needed
  $("#nptitle").html(data["cursong"]["title"]);
  $("#npartist").html(data["cursong"]["artist"]);

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
    url:"/control/playpause"
  });
});

$("#nextbutton").button({text: false, icons:{primary:'ui-icon-wetunes-next'}})
.click(function(){
  $.ajax({
    url:"/control/next"
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
var t = setInterval("header_ajax()", 1000);
    
}); // document ready

// vim: ft=javascript sw=2 ts=2 et
