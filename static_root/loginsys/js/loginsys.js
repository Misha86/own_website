$(function() {
    var lang_cod = $('#lang_cod').text()
    //var cod = document.getElementById('cod').textContent;
    $.datepicker.setDefaults( $.datepicker.regional[ lang_cod ])
    $("#id_date_of_birth").datepicker(
        {changeMonth: true,
            changeYear: true,
            dateFormat: "yy-mm-dd",
            //showOn: "both",
            showWeek: true,
            yearRange: "1920:"

        });
});

//$( function() {
//    $( "#login" ).dialog({
//        autoOpen: false,
//        width: 400,
//        show: {
//          effect: "blind",
//          duration: 1000
//        },
//        hide: {
//          effect: "explode",
//          duration: 1000
//        }
//        //buttons: [
//        //    {
//        //        text: "Ok",
//        //        click: function() {
//        //            $( this ).dialog( "close" );
//        //        }
//        //    },
//        //    {
//        //        text: "Cancel",
//        //        click: function() {
//        //            $( this ).dialog( "close" );
//        //        }
//        //    }
//        //]
//    });
//
//    $( "#opener" ).click(function( event ) {
//        $( "#login" ).dialog( "open" );
//        event.preventDefault();
//    });
//    $( "#cancel" ).click(function() {
//        $( "#login" ).dialog( "close" );
//    });
//});