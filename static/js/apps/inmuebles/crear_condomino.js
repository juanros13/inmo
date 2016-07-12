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
var CrearCondominoManaged = function () {

    var initCrearCondomino = function () {

        var selectPais = $('#id_pais');
        var selectEstado = $('#id_estado');
        var selectMunicipio = $('#id_municipio');
        var selectColonia = $('#id_colonia');
        var estado = 0;

        selectPais.change(function() {
            $.ajax({
                url:   '/poblacion/estado/'+this.value+'/',
                type:  'post',
                //beforeSend: function () {
                //    $("#resultado").html("Procesando, espere por favor...");
                //},
                success:  function (response) {
                    selectEstado.append('<option value="" selected>----- Selecciona el estado -----</option>');
                    $.each(response.estados,function(key, value) 
                    {
                        selectEstado.append('<option value=' + value.clave_estado+ '>' + value.nombre + '</option>');
                        
                    });
                    selectEstado.selectpicker('refresh');
                }
            });
        });
        selectEstado.change(function() {
            $.ajax({
                url:   '/poblacion/municipio/'+this.value+'/',
                type:  'post',
                //beforeSend: function () {
                //    $("#resultado").html("Procesando, espere por favor...");
                //},
                success:  function (response) {
                    selectMunicipio.append('<option value="" selected>----- Selecciona el municipio -----</option>');
                    $.each(response.municipios,function(key, value) 
                    {
                        selectMunicipio.append('<option value=' + value.clave_municipio+ '>' + value.nombre + '</option>');
                    });
                    selectMunicipio.selectpicker('refresh');
                }
            });
        });
        selectMunicipio.change(function() {
            $.ajax({
                url:   '/poblacion/colonia/'+selectEstado.val()+'/'+this.value+'/',
                type:  'post',
                //beforeSend: function () {
                //    $("#resultado").html("Procesando, espere por favor...");
                //},
                success:  function (response) {
                    selectColonia.append('<option value="" selected>----- Selecciona una colonia -----</option>');
                    $.each(response.colonias,function(key, value) 
                    {
                        selectColonia.append('<option value=' + value.id+ '>' + value.nombre + '</option>');
                    });
                    selectColonia.selectpicker('refresh');
                }
            });
        });
    }
    return {

        //main function to initiate the module
        init: function () {
            initCrearCondomino();
        }

    };
}();
var FormValidation = function () {

    // basic validation
    var handleValidation1 = function() {
        // for more info visit the official plugin documentation: 
            // http://docs.jquery.com/Plugins/Validation

            var form1 = $('#form_crear_condomino');
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
                    email: {
                        required: true,
                        email:true
                    },
                    password: {
                        required: true,
                    },
                    password2: {
                        required: true,
                    },
                    first_name: {
                        required: true,
                    },
                    last_name: {
                        required: true,
                    },
                },

                invalidHandler: function (event, validator) { //display error alert on form submit              
                    success1.hide();
                    error1.show();
                    App.scrollTo(error1, -200);
                    toastr["error"]("tienes algunos errores en la forma", "Mensaje");
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
    CrearCondominoManaged.init();
    FormValidation.init();
});
