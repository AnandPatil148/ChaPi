function updateRoomList(data) 
{
    var dropdownOptionsHtml = '';

    // Generate HTML for dropdown options based on data
    data.forEach(
    function (option)
    {
        dropdownOptionsHtml += '<li><a class="dropdown-item" href="/room/' + option + '/">' + option + ' Room</a></li>';
    });

    // Insert the generated HTML into the placeholder element
    document.getElementById('dropdownOptionsPlaceholder').innerHTML = dropdownOptionsHtml;
}
