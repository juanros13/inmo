var TableDatatablesManaged = function () {

    var initTableDirectorio = function () {

        var table = $('.table-departementos');
        // Setup - add a text input to each footer cell
         $('.table-departementos tfoot th').each( function () {
            var title = $(this).text();
            $(this).html( '<input type="text" class="form-control" placeholder="Buscar '+title+'" />' );
        });

        // begin first table
        var tableDepartamento = table.DataTable({

            // Internationalisation. For more info refer to http://datatables.net/manual/i18n
         

            // Or you can use remote translation file
            "language": {
               url: '//cdn.datatables.net/plug-ins/3cfcc339e89/i18n/Spanish.json'
            },

            // Uncomment below line("dom" parameter) to fix the dropdown overflow issue in the datatable cells. The default datatable layout
            // setup uses scrollable div(table-scrollable) with overflow:auto to enable vertical scroll(see: assets/global/plugins/datatables/plugins/bootstrap/dataTables.bootstrap.js). 
            // So when dropdowns used the scrollable div should be removed. 
            //"dom": "<'row'<'col-md-6 col-sm-12'l><'col-md-6 col-sm-12'f>r>t<'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>",

             // setup buttons extentension: http://datatables.net/extensions/buttons/
            buttons: [
                { extend: 'print', className: 'btn dark btn-outline' },
                { extend: 'pdf', className: 'btn green btn-outline' },
                { extend: 'csv', className: 'btn purple btn-outline ' }
            ],

            // setup responsive extension: http://datatables.net/extensions/responsive/
            responsive: {
                details: {
                   
                }
            },

            "order": [
                [0, 'asc']
            ],
            
            "lengthMenu": [
                [5, 10, 15, 20, -1],
                [5, 10, 15, 20, "All"] // change per page values here
            ],
            // set the initial value
            "pageLength": 10,

            "dom": "<'row' <'col-md-12'B>><'row'<'col-md-6 col-sm-12'l><'col-md-6 col-sm-12'f>r><'table-scrollable't><'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>", // horizobtal scrollable datatable

        });
        tableDepartamento.buttons().container()
            .appendTo( $('.wololo', tableDepartamento.table().container() ) );
        // Apply the search
        tableDepartamento.columns().eq(0).each(function (colIdx) {
            $('input', tableDepartamento.column(colIdx).footer()).on('keyup change', function () {
                tableDepartamento.column (colIdx)
                         .search (this.value.replace(/;/g, "|"), true, false)
                         .draw ();
            } );
        } );

    }
    return {

        //main function to initiate the module
        init: function () {
            if (!jQuery().dataTable) {
                return;
            }

            initTableDirectorio();
        }

    };
}();
jQuery(document).ready(function() {
    TableDatatablesManaged.init();
});
