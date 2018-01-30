$(document).ready(function() {
    $('#table-filter').on('keyup', function() {
        var value = $(this).val().toLowerCase();
        $('#limits-table tbody tr td ul li').filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });

        $('#limits-table tbody tr').each(function() {
            $(this).show();
            if ($(this.children[1].children[0]).children(':visible').length == 0) {
                $(this).hide();
            }
        });
    });
});
