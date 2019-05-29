$(document).ready(function() {
  $("form").submit(function() {
    $(this)
      .find(":input[type=submit]")
      .prop("disabled", true)
      .val("Working...");
  });
});
