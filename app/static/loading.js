let pings = 0;

function checkProgress() {
  $.get("/api/checkProgress", { uuid: uuid }, function(data) {
    pings++;
    $("#pings").text(pings);
    $("#latestResponse").text(JSON.stringify(data));
    if (data.ready) {
      window.location.replace("/opinion?uuid=" + uuid);
    }
  });
}

$(document).ready(function() {
  $("#uuid").text("UUID: " + uuid);

  setInterval(checkProgress, 2000);
});
