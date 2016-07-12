jQuery.extend(jQuery.validator.messages, {
      required: "Este campo es obligatorio.",
      remote: "Por favor, rellena este campo.",
      email: "Por favor, escribe una dirección de correo válida",
      url: "Por favor, escribe una URL válida.",
      date: "Por favor, escribe una fecha válida.",
      dateISO: "Por favor, escribe una fecha (ISO) válida.",
      number: "Por favor, escribe un número entero válido.",
      digits: "Por favor, escribe sólo dígitos.",
      creditcard: "Por favor, escribe un número de tarjeta válido.",
      equalTo: "Por favor, escribe el mismo valor de nuevo.",
      accept: "Por favor, escribe un valor con una extensión aceptada.",
      maxlength: jQuery.validator.format("Por favor, no escribas más de {0} caracteres."),
      minlength: jQuery.validator.format("Por favor, no escribas menos de {0} caracteres."),
      rangelength: jQuery.validator.format("Por favor, escribe un valor entre {0} y {1} caracteres."),
      range: jQuery.validator.format("Por favor, escribe un valor entre {0} y {1}."),
      max: jQuery.validator.format("Por favor, escribe un valor menor o igual a {0}."),
      min: jQuery.validator.format("Por favor, escribe un valor mayor o igual a {0}.")
    });
var TableDatatablesManaged = function () {

    var initTableDirectorio = function () {

        var table = $('.directorio');

        // begin first table
        table.dataTable({

            // Internationalisation. For more info refer to http://datatables.net/manual/i18n
            "language": {
                "aria": {
                    "sortAscending": ": activate to sort column ascending",
                    "sortDescending": ": activate to sort column descending"
                },
                "emptyTable": "No hay datos disponibles en la tabla",
                "info": "Mostrando del _START_ hasta _END_ de _TOTAL_ registros",
                "infoEmpty": "No se encontraron registros",
                "infoFiltered": "(filtered 1 from _MAX_ total records)",
                "lengthMenu": "Mostrar _MENU_",
                "search": "Buscar:",
                "zeroRecords": "No se encontraton coincidencias",
                "paginate": {
                    "previous":"Anterior",
                    "next": "Siguiente",
                    "last": "Ultima",
                    "first": "Primera"
                }
            },

            // Or you can use remote translation file
            //"language": {
            //   url: '//cdn.datatables.net/plug-ins/3cfcc339e89/i18n/Portuguese.json'
            //},

            // Uncomment below line("dom" parameter) to fix the dropdown overflow issue in the datatable cells. The default datatable layout
            // setup uses scrollable div(table-scrollable) with overflow:auto to enable vertical scroll(see: assets/global/plugins/datatables/plugins/bootstrap/dataTables.bootstrap.js). 
            // So when dropdowns used the scrollable div should be removed. 
            //"dom": "<'row'<'col-md-6 col-sm-12'l><'col-md-6 col-sm-12'f>r>t<'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>",

            "bStateSave": true, // save datatable state(pagination, sort, etc) in cookie.

            //"columnDefs": [ {
            //    "targets": 0,
            //    "orderable": false,
            //    "searchable": false
            //}],

            "lengthMenu": [
                [5, 15, 20, -1],
                [5, 15, 20, "All"] // change per page values here
            ],
            // set the initial value
            "pageLength": 20,            
            //"columnDefs": [{  // set default column settings
            //    'orderable': false,
            //    'targets': [0]
            //}, {
            //    "searchable": true,
            //    "targets": [0]
            //}],
            "order": [
                [1, "asc"]
            ] // set first column as a default sort by asc
        });

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
var FormValidation = function () {

    // basic validation
    var handleValidation1 = function() {
        // for more info visit the official plugin documentation: 
            // http://docs.jquery.com/Plugins/Validation

            var form1 = $('#form_crear_directorio');
            var error1 = $('.alert-danger', form1);
            var success1 = $('.alert-success', form1);

            form1.validate({
                errorElement: 'span', //default input error message container
                errorClass: 'help-block help-block-error', // default input error message class
                focusInvalid: false, // do not focus the last invalid input
                ignore: "",  // validate all fields including form hidden input
                messages: {
                    select_multi: {
                        maxlength: jQuery.validator.format("Max {0} items allowed for selection"),
                        minlength: jQuery.validator.format("At least {0} items must be selected")
                    }
                },
                rules: {
                    nombre: {
                        required: true,
                    },
                    telefono: {
                        required: true,
                    },
                },

                invalidHandler: function (event, validator) { //display error alert on form submit              
                    success1.hide();
                    error1.show();
                    App.scrollTo(error1, -200);
                },

                highlight: function (element) { // hightlight error inputs
                    $(element)
                        .closest('.form-group').addClass('has-error'); // set error class to the control group
                },

                unhighlight: function (element) { // revert the change done by hightlight
                    $(element)
                        .closest('.form-group').removeClass('has-error'); // set error class to the control group
                },

                success: function (label) {
                    label
                        .closest('.form-group').removeClass('has-error'); // set success class to the control group
                },

                submitHandler: function (form) {
                    //success1.show();
                    error1.hide();
                    submit();
                }
            });


    }
    return {
        //main function to initiate the module
        init: function () {

            handleValidation1();

        }

    };

}();
jQuery(document).ready(function() {
    TableDatatablesManaged.init();
    FormValidation.init();
});
