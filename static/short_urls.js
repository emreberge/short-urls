// Executed when the document has loaded.
$(document).ready(function() {
    initilizeShortenUrlForm();
    focusOnFirstInputOfFirstForm();
});

function initilizeShortenUrlForm() {
    $('#shortenUrlForm').submit(submitSortenUrlForm);
}

function focusOnFirstInputOfFirstForm() {
    var $firstForm = $(document).find('form').filter(':first');
    var $firstInput = $firstForm.find('input').filter(':first');
    $firstInput.focus();
}

function submitSortenUrlForm(event) {
    event.preventDefault();
    var form = retrieveAddressAndActionFromForm($(this));

    $.post(form.action, form.params)
    .success(function(data) {
        addShortUrlToList(data.short_url, form.params.url_address);
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

function addShortUrlToList(shortUrl, longUrl) {
    var href = urlByAppendUrlToLocation(shortUrl);
    var $listItem = $('<li>' + longUrl + ' <a href="' + href +'">' + href + '</a>');
    $('#result').prepend($listItem);
    appendClippyToElement($listItem, href);
}

function appendClippyToElement($element, copyUrl) {
    var $clippy = $('<span>' + copyUrl + '</span>')
    $element.append($clippy);
    $clippy.clippy();
}

function urlByAppendUrlToLocation(url) {
    //If attr href is used '/#' will break the page
    return $(location).attr('host') + '/' + url;
}

function displayErrorForUrl(url) {
    alert(''.concat('The url: "', url, '" is not valid or an allowed address.'));
}