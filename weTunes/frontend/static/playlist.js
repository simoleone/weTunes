function playlist_ajax()
{
  $.ajax({
    url:"/ajax/playlist",
  dataType: 'json',
  success: playlist_update
  });
}

function playlist_update(data)
{
  $("#tmp_content").remove();
  $("<div class='content' id='tmp_content' style='display: none;'></div>").insertAfter("#main_content");
  tmp_content = $("#tmp_content");
  
  for(var i=0; i<data.length ; i++) {
    var tmp = "<div class='playlist_block'>";
    for (var j=0; j<data[i]['tracks'].length ; j++) {
      tmp += "<span class='playlist_track'>";
      tmp += data[i]['tracks'][j]['artist'] + " - ";
      tmp += data[i]['tracks'][j]['album'] + " - ";
      tmp += data[i]['tracks'][j]['title'] + " - ";
      tmp += "</span>";
    }

    tmp += "<span class='playlist_author'>";
    tmp += data[i]['author'];
    tmp += "</span>";

    // TODO: add logic for whether voted or not
    //       also shorten if it doesnt fit
    tmp += "<span class='playlist_vote'><a href='#'>";
    tmp += data[i]['voted'] ? "-" : "+" ;
    tmp += "</a></span>";

    tmp += "</div>";
    tmp_content.append(tmp);
  }
  $("div.content").fadeToggle();
  $("#main_content").remove();
  tmp_content.attr("id", "main_content");
}



$(document).ready(function(){
  var t = setInterval("playlist_ajax()", 5000);
}); // document ready

// vim: ft=javascript sw=2 ts=2 et
