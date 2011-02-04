function search_ajax(term) {
  $.ajax({
    type: "POST",
    url: "/ajax/search",
    data: {"field":"any", "value":term},
    success: search_process,
    dataType: "json"
  }); // ajax
}

function search_process(data) {
  $("#searchresults_auto").fadeOut("fast", function() {
    $("#searchresults_auto").html("");
    for (s in data) {
      // TODO: store track, file, album, artist in a way that can be sorted and retrieved
      $("#searchresults_auto").append("<span class='playlist_track'>"+data[s].title+"</span>");
    }
    $("#searchresults_auto").fadeIn();
  });
}

function sortsearch(by) {
  // TODO: implement a sort that looks sexy
}

$(document).ready(function(){

  // if we came to this page from a post, initiate the search and prepopulate the box
  if ($("#initsearchterm").text().length > 0) {
    $("#searchbox input[name=searchterm]").val($("#initsearchterm").text());
    search_ajax($("#initsearchterm").text());
  }
  
  // rewire the search box to be an ajax call instead
  $("#searchform").submit(function(){
    search_ajax($("#searchbox input[name=searchterm]").val());
    return false;
  });

  // wire up the search buttons
  $("#sortby_artist").click(function(){
    sortsearch('artist');
  });
  $("#sortby_album").click(function(){
    sortsearch('album');
  });
  $("#sortby_title").click(function(){
    sortsearch('title');
  });

  // wire up the playlist submission button
  $("#submitbutton").click(function(){
    // TODO: configure submission via ajax call
  });
  
  // TODO: set up drag and drop support
  // TODO: set up reordering support for playlist

}); // document ready

// vim: ft=javascript sw=2 ts=2 et
