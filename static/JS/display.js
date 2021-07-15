$(document).ready(function () {
    $('#events_table').DataTable({
        "order": [[2, "asc"]],
        "pagingType": "numbers"

    });
});