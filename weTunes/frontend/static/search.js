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
    $("#searchresults_auto").children().remove();
    for (s in data) {
      var html = "<li class='searchitem'>";
      html += "<span class='artist'>"+ data[s].artist +"</span>";
      html += "<span class='album'>"+ data[s].album +"</span>";
      html += "<span class='title'>"+ data[s].title +"</span>";
      html += "<span class='filename'>"+ data[s].file +"</span>";
      html += "</li>";
      $("#searchresults_auto").append(html);
    }
    $(".searchitem").draggable({ scroll: false,
                                 revert: 'invalid',
                                 helper: 'clone',
                                 appendTo: '#playlistcreator_auto',
                                 zIndex:'500',
                                 connectToSortable: '#playlistcreator_auto'
                               });
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

  // wire up the playlist submission and clear buttons
  $("#submitbutton").click(function(){
    var arr = [];
    $("#playlistcreator_auto .searchitem .filename").each(function(){arr.push($(this).text());});
    $.ajax({
      type: "POST",
      url: "/ajax/createblock",
      data: JSON.stringify(arr),
      success: function(){$("#clearbutton").click();}
    }); // ajax
  });
  $("#clearbutton").click(function(){
    $("#playlistcreator_auto").children().fadeOut("fast", function(){
      $(this).remove();
    });
  });  

  // set up the playlist creator
  $("#playlistcreator_auto").sortable();

  // TODO: set up reordering support for playlist

}); // document ready

// vim: ft=javascript sw=2 ts=2 et
