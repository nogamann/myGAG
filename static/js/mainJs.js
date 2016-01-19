$('#submit').click(function()
{
    var numOfMemes = 20;
    var selectedVal = "";
    for (var i = 1; i < numOfMemes + 1; i++){
        var selected = $("input[type='radio'][name='button"+ i +"']:checked");
        if (selected.length > 0) {
            selectedVal += selected.val() + ';';
        }
    }

    $.get( "/submit", {selectedVal: selectedVal } ,function(res){
        var listings = $.parseJSON(res);
        var jsonLen = listings.length;
        var inner = "";
        var curRes;
        for (var i = 0; i < jsonLen; i++){
            curRes = listings[i];
            var img = curRes[0];
            var title = curRes[1];
            inner += "<div class='row mt centered' id='div" + i +"'><div class='col-lg-6 col-lg-offset-3' style='margin-top:0px'><h1 style='margin-top:0px'>"
            + title + "</h1><img src='"
            + img + "' width='500'></div></div><div class='row'></div>";
           }
        document.getElementById("resultContainer").innerHTML=inner;
    });

});

$body = $("body");

$(document).on({
    ajaxStart: function()
    {
        $body.addClass("loading");
    },
    ajaxStop: function() {
        $body.removeClass("loading");

        if (a ==  1) {
        $('html, body').animate({scrollTop:18250},1000);
        }
    }
});

$('#submit').click(function(){
       a = 1;
        $('html, body').animate({scrollTop:18250},1000);

    return false;
});

var a = 0;