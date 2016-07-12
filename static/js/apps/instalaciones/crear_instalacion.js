var ComponentsInstalaciones = function () {

  
  var handleInstalaciones = function () {

    if (jQuery().timepicker) {
      $('.timepicker-default').timepicker({
        autoclose: true,
        showSeconds: true,
        minuteStep: 1
      });

      $('.timepicker-no-seconds').timepicker({
        autoclose: true,
        minuteStep: 15
      });

      $('.timepicker-24').timepicker({
        autoclose: true,
        minuteStep: 15,
        showSeconds: false,
        showMeridian: false
      });

      // handle input group button click
      $('.timepicker').parent('.input-group').on('click', '.input-group-btn', function(e){
        e.preventDefault();
        $(this).parent('.input-group').find('.timepicker').timepicker('showWidget');
      });
      $('.dia-disponible').click(function(){
        var row = $(this).closest('tr');
        if($(this).is(':checked')) {  
          row.removeClass('active');
          row.find('.hora-hasta').val('00:00').attr('readonly', false).removeAttr("disabled");
          row.find('.hora-desde').val('00:00').attr('readonly', false).removeAttr("disabled");
          row.find('.disponible-todo-el-dia').removeAttr("disabled");
          $.uniform.update();
        } else {  
          row.addClass('active');
          row.find('.hora-hasta').val('00:00').attr('readonly', true).attr("disabled", true);
          row.find('.hora-desde').val('00:00').attr('readonly', true).attr("disabled", true);
          row.find('.disponible-todo-el-dia').prop( "checked", false );
          row.find('.disponible-todo-el-dia').attr("disabled", true);
          $.uniform.update();
        }  

      });
      $('.disponible-todo-el-dia').click(function(){
        var row = $(this).closest('tr');
        if($(this).is(':checked')) {  
          row.find('.hora-hasta').val('00:00');
          row.find('.hora-desde').val('00:00');
        } 

      });
      $('.hora-hasta').change(function(){
        var row = $(this).closest('tr');
        row.find('.disponible-todo-el-dia').prop( "checked", false );
        $.uniform.update();
      });
    }
  }


  return {
    //main function to initiate the module
    init: function () {
      handleInstalaciones();
    }
  };

}();

jQuery(document).ready(function() {    
  ComponentsInstalaciones.init(); 
});
