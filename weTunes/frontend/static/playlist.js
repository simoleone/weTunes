function playlist_ajax()
{
  $.ajax({
    url:"/ajax/playlist",
  dataType: 'json',
  success: playlist_update
  });
}

function markup_song(s) {
  var html = "<li class='searchitem'>";
  html += "<span class='artist'><a href='#' class='browse_artist'>"+ s['artist'] +"</a></span>";
  html += "<span class='album'><a href='#' class='browse_album'>"+ s['album'] +"</a></span>";
  html += "<span class='title'>"+ s['title'] +"</span>";
  html += "</li>";
  return html;
}

function playlist_update(data)
{
  $("#tmp_content").remove();
  $("<div class='content' id='tmp_content' style='display: none;'></div>").insertAfter("#main_content");
  tmp_content = $("#tmp_content");
  
  for(var i=0; i<data.length ; i++) {
    var tmp = "<div class='playlist_block'><ul>";
    for (var j=0; j<data[i]['tracks'].length ; j++) {
      tmp += markup_song(data[i]['tracks'][j]);
    }

    tmp += "</ul><span class='playlist_author'>";
    tmp += data[i]['author'];
    tmp += "</span>";

    tmp += "<span class='playlist_vote'><a href='#' class='votebutton'>";
    if(data[i]['voted']){
      tmp += "-";
    } else {
      tmp += "+";
    }
    tmp += "</a>";
    tmp += "<span class='blkid' style='display:none;'>"+data[i]['id']+"</span>";
    tmp += "</span>";

    tmp += "</div>";
    tmp_content.append(tmp);
  }

  // wire up the new vote buttons
  $("#tmp_content .votebutton").click(function(){
    $(this).fadeOut();
    var url;
    var blkid = $(this).siblings(".blkid").text();
    if($(this).text() == "-") {
      url = "/ajax/unvote/" + blkid;
    } else {
      url = "/ajax/vote/" + blkid;
    }
    $.ajax({
      url: url
      });
  });

  $("div.content").toggle();
  $("#main_content").remove();
  tmp_content.attr("id", "main_content");
}



$(document).ready(function(){
  var t = setInterval("playlist_ajax()", 5000);
}); // document ready

// vim: ft=javascript sw=2 ts=2 et
