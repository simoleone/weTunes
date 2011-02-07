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
  

  // TODO: shorten track strings if they're uber long
  for(var i=0; i<data.length ; i++) {
    var tmp = "<div class='playlist_block'>";
    for (var j=0; j<data[i]['tracks'].length ; j++) {
      tmp += "<span class='playlist_track'>";
      tmp += data[i]['tracks'][j]['artist'] + " - ";
      tmp += data[i]['tracks'][j]['album'] + " - ";
      tmp += data[i]['tracks'][j]['title'];
      tmp += "</span>";
    }

    tmp += "<span class='playlist_author'>";
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
