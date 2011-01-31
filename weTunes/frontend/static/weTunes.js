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
$("#npprogressbar").progressbar({'value':50});


//////////////////////////////////////
// control buttons
//////////////////////////////////////
$("#playpausebutton").button({text: false, icons:{primary:'ui-icon-wetunes-play'}})
$("#nextbutton").button({text: false, icons:{primary:'ui-icon-wetunes-next'}})


//////////////////////////////////////
// volume slider
//////////////////////////////////////
$("#volumeslider").slider({ orientation: 'vertical', max: 100, min: 0 });

}); // document ready
