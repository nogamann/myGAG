$('#submit').click(function()
{
    var numOfMemes = 3;
    var selectedVal = "";
    for (var i = 1; i < numOfMemes + 1; i++){
        var selected = $("input[type='radio'][name='"+ i +"']:checked");
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
            inner += "<div class='row mt centered'><div class='col-lg-6 col-lg-offset-3' style='margin-top:0px'><h1 style='margin-top:0px'>meme</h1><img src='"
            + curRes + "' width='500'></div></div><div class='row'></div>";
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

//        $('html, body').animate({scrollTop:950},1000);
    }
});

$('#scrollDown').click(function(){
    $('html, body').animate({
        scrollTop: $( $.attr(this, 'href') ).offset().top
    }, 'slow');
    return false;
});
