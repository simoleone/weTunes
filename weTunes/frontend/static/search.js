function search_ajax(term) {
  $.ajax({
    type: "POST",
    url: "/ajax/search",
    data: {"field":"any", "value":term},
    success: search_process,
    dataType: "json"
  }); // ajax
}

function browse_ajax(field, term) {
  $.ajax({
    type: "POST",
    url: "/ajax/search",
    data: {"field":field, "value":term},
    success: search_process,
    dataType: "json"
  }); // ajax
}


function random_ajax() {
  $.ajax({
    type: "POST",
    url: "/ajax/random",
    success: search_process,
    dataType: "json"
  }); // ajax
}

function markup_song(s) {
  var html = "<li class='searchitem'>";
  html += "<span class='artist'><a href='#' class='browse_artist'>"+ s.artist +"</a></span>";
  html += "<span class='album'><a href='#' class='browse_album'>"+ s.album +"</a></span>";
  html += "<span class='title'>"+ s.title +"</span>";
  html += "<span class='filename'>"+ s.file +"</span>";
  html += "</li>";
  return html;
}

function search_process(data) {
  $("#searchresults_auto").fadeOut("fast", function() {
    $("#searchresults_auto").children().remove();
    for (s in data) {
      $("#searchresults_auto").append(markup_song(data[s]));
    }
    $(".searchitem").draggable({ scroll: false,
                                 revert: 'invalid',
                                 helper: 'clone',
                                 appendTo: '#playlistcreator_auto',
                                 zIndex:'500',
                                 connectToSortable: '#playlistcreator_auto'
                               });
    $(".browse_artist").each(function(i, e){
     $(e).click(function(){
       browse_ajax('artist', $(e).text());
     })
    });
    $(".browse_album").each(function(i, e){
     $(e).click(function(){
       browse_ajax('album', $(e).text());
     })
    });
    $("#searchresults_auto").fadeIn();
  });
}

// does an animated insertion sort
function sortsearch(by) {
  var q = "." + by;
  return sortsearch_helper(q, 0);
}

function sortsearch_helper(q, pos) {
  var parent_node = $("#searchresults_auto");
  var items = $(".searchitem", parent_node);

  if (pos >= items.length) {
    return;
  }

  var cur = pos;
  var cur_val = $(q, items[cur]).text();
  for(i=pos+1; i < items.length ; i++) {
    var i_val = $(q, items[i]).text();
    if(i_val < cur_val) {
      cur_val = i_val;
      cur = i;
    }
  }

  if (cur != pos) {
    var tmp = $(items[cur]);
    tmp.hide('slide',{},125,function(){
      tmp.detach();
      tmp.insertBefore(items[pos]);
      tmp.show('slide',{},125, function(){sortsearch_helper(q, ++pos)});
    });
  } else {
    sortsearch_helper(q, ++pos);
  }
}

$(document).ready(function(){

  // if we came to this page from a post, initiate the search and prepopulate the box
  if ($("#initsearchterm").text().length > 0) {
    $("#searchbox input[name=searchterm]").val($("#initsearchterm").text());
    search_ajax($("#initsearchterm").text());
  } else if ($("#initbrowsevalue").text().length > 0) {
    // if we came to this page from a /browse/<field>/<query>
    $("#searchbox input[name=searchterm]").val($("#initbrowsevalue").text());
    browse_ajax($("#initbrowsefield").text(), $("#initbrowsevalue").text());
  } else {
    random_ajax();
  }
  
  // rewire the search box to be an ajax call instead
  $("#searchform").submit(function(){
    search_ajax($("#searchbox input[name=searchterm]").val());
    return false;
  });

  $("#fill_random").click(function(){
    random_ajax();
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
      success: function() {
        $("#clearbutton").click();
        header_ajax();
      }
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
