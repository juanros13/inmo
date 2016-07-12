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

        if ($('#calendar').width() <= 400) {
            $('#calendar').addClass("mobile");
            h = {
              left: 'title, prev, next',
              center: '',
              right: 'today,month,agendaWeek,agendaDay'
            };
        } else {
          $('#calendar').removeClass("mobile");
          if (App.isRTL()) {
            h = {
              right: 'title',
              center: '',
              left: 'prev,next,today,month,agendaWeek,agendaDay'
            };
          } else {
            h = {
              left: 'title',
              center: '',
              right: 'prev,next,today,month,agendaWeek,agendaDay'
            };
          }
        }

        $('#calendar').fullCalendar('destroy'); // destroy the calendar
        $('#calendar').fullCalendar({ //re-initialize the calendar
          lang: 'es',
          disableDragging: true,
          header: h,
          editable: false,
          eventClick: function (calEvent, jsEvent, view) {
            var view_name=view.name;
            if(view_name=='month')
            {
              $('#calendar').fullCalendar('gotoDate', calEvent.start);
              $('#calendar').fullCalendar( 'changeView', 'agendaDay'  );
            }
          },
        });
      }
    };
}();

jQuery(document).ready(function() {    
   AppCalendar.init(); 
});