let pings = 0;

function checkProgress() {
  $.get("/api/checkProgress", function(data) {
    pings++;
    $("#pings").text(pings);
    $("#latestResponse").text(JSON.stringify(data));
    if (data.ready) {
      window.location.replace("/opinion");
    }
  });
}

$(document).ready(function() {
  setInterval(checkProgress, 2000);
});
