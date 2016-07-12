var ComponentsInstalaciones = function () {

    var handleDatePickers = function () {

    if (jQuery().datepicker) {
        $('.date-picker').datepicker({
            rtl: App.isRTL(),
            orientation: "left",
            autoclose: true,
            language:'es',
            format: 'yyyy-mm-dd',
        });
        //$('body').removeClass("modal-open"); // fix bug when inline picker is used in modal
    }

    /* Workaround to restrict daterange past date select: http://stackoverflow.com/questions/11933173/how-to-restrict-the-selectable-date-ranges-in-bootstrap-datepicker */
    }
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
        }
    }
    return {
        //main function to initiate the module
        init: function () {
          handleInstalaciones();
          handleDatePickers();
        }
    };

}();
var AppCalendar = function() {

    return {
        //main function to initiate the module
        init: function() {
            this.initCalendar();
        },

        initCalendar: function() {

            if (!jQuery().fullCalendar) {
                return;
            }

            var date = new Date();
            var d = date.getDate();
            var m = date.getMonth();
            var y = date.getFullYear();

            var h = {};

            if (App.isRTL()) {
                if ($('#calendar').parents(".portlet").width() <= 720) {
                    $('#calendar').addClass("mobile");
                    h = {
                        right: 'title, prev, next',
                        center: '',
                        left: 'agendaDay, agendaWeek, month, today'
                    };
                } else {
                    $('#calendar').removeClass("mobile");
                    h = {
                        right: 'title',
                        center: '',
                        left: 'agendaDay, agendaWeek, month, today, prev,next'
                    };
                }
            } else {
                if ($('#calendar').parents(".portlet").width() <= 720) {
                    $('#calendar').addClass("mobile");
                    h = {
                        left: 'title, prev, next',
                        center: '',
                        right: 'today,month,agendaWeek,agendaDay'
                    };
                } else {
                    $('#calendar').removeClass("mobile");
                    h = {
                        left: 'title',
                        center: '',
                        right: 'prev,next,today,month,agendaWeek,agendaDay'
                    };
                }
            }

            

            $('#calendar').fullCalendar('destroy'); // destroy the calendar
            var calendar = $('#calendar').fullCalendar({ //re-initialize the calendar
                lang: 'es',
                header: h,
                defaultView: 'agendaWeek', // change default view with available options from http://arshaw.com/fullcalendar/docs/views/Available_Views/ 
                slotMinutes: 15,
                editable: false,
                disableDragging:true,
                droppable: false, // this allows things to be dropped onto the calendar !!!
                eventRender: function (event, element) {
                    var propValue;
                    for(var propName in event) {
                        propValue = event[propName]

                        console.log(propName,propValue);
                    }
                    element.popover({
                        title: event.title,
                        placement: 'right',
                        html : true,
                        content: 'Dia del evento: ' + String(event.start.toISOString().slice(0, 10)) + '<br\/>Descripcion: ' + event.description,
                    });
                }
            });

        }

    };

}();

jQuery(document).ready(function() {    
   AppCalendar.init(); 
   ComponentsInstalaciones.init(); 
});