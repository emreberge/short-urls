// Executed when the document has loaded.
$(document).ready(function() {
    initilizeShortenUrlForm();
});

function initilizeShortenUrlForm() {
    $("#shortenUrlForm").submit(submitSortenUrlForm);
}

function submitSortenUrlForm(event) {
    event.preventDefault();
    var form = retrieveAddressAndActionFromForm($(this));

    $.post(form.action, form.params)
    .success(function(data) {
        addShortUrlToTable(data.short_url, form.params.url_address);
    })
    .error(function() {
       displayErrorForUrl(form.params.url_address);
    });

}

function retrieveAddressAndActionFromForm($form) {
    return {
        action: $form.attr('action'),
        params: {
            url_address: $form.find('input[name="url_address"]').val()
        }
    }
}

function addShortUrlToTable(shortUrl, longUrl) {
    $("#result").prepend("<tr><td>" + longUrl + "</td><td>" + shortUrl + "</td><tr>");
}

function displayErrorForUrl(url) {
    alert("".concat('The url: "', url, '" is not valid or an allowed address.'));
}