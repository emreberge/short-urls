$(document).ready(function() {
    $("#shortenUrlForm").submit(function(event) {
        event.preventDefault();

        var $form = $(this),
        term = $form.find('input[name="url_address"]').val(),
        url = $form.attr('action');

        $.post(url, {
            url_address: term
        },
        function(data) {
            var content = data.short_url;
            $("#result").empty().append(content);
        }
        ).error(
        function() {
            alert("".concat('The url: ', term, ' is not valid or an allowed address.'));
        });
    });
});