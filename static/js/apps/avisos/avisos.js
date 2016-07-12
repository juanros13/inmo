var ComponentsEditors = function () {
    

    var handleSummernote = function () {
        $('#id_contenido').summernote({height: 300});
        //API:
        //var sHTML = $('#summernote_1').code(); // get code
        //$('#summernote_1').destroy(); // destroy
    }

    return {
        //main function to initiate the module
        init: function () {
            handleSummernote();
        }
    };

}();

jQuery(document).ready(function() {    
   ComponentsEditors.init(); 
});