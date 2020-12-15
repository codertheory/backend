function newsletterSubscribe(url) {
    let form = $("#subscribe-form");
    $.ajax({
        type: "POST",
        url: url,
        enctype: "multipart/form-data",
        data: new FormData(form[0]),
        processData: false,
        contentType: false,
        success: function (data, status, xhr) {
            alert(`You've successfully subscribed`)
        }
    });
    return false;
}
