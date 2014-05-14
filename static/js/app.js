$(function () {
    var data_inicial = $('#data_inicial');
    var data_final = $('#data_final');
    var hoje = new Date();
    
    data_inicial.datepicker({dateFormat: "dd/mm/yy"});
    data_final.datepicker({dateFormat: "dd/mm/yy"});
    data_inicial.datepicker('setDate', hoje);
    data_final.datepicker('setDate', hoje);

    $('#form1').submit(function(event){
        $.post(
            this.action, 
            $(this).serialize(), 
            function(data){
               console.log(data);
               var iframe = document.getElementById('iframex');
               iframe.src='static/output.pdf';
            });
        return false; //do not submit form the normal way
    });
});

