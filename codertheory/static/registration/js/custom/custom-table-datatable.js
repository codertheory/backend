/*
---------------------------------------
    : Custom - Table Datatable js :
---------------------------------------
*/
"use strict";
$(document).ready(function () {
    /* -- Table - Datatable -- */
    $('#datatable').DataTable({
        responsive: true
    });
    $('#result_list').DataTable({
        responsive: true,
        paging: false,
        searching: false,
        select: true,
        info: false
    });
    $('#default-datatable').DataTable({
        "order": [[3, "desc"]],
        responsive: true
    });
    var table = $('#datatable-buttons').DataTable({
        lengthChange: false,
        responsive: true,
        buttons: ['copy', 'csv', 'excel', 'pdf', 'print']
    });
    table.buttons().container().appendTo('#datatable-buttons_wrapper .col-md-6:eq(0)');
});
