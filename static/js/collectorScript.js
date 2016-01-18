/**
 * Created by Erez Levanon on 25/11/2015.
 */
var curFoodId = 1;
var curMovieId = 2;

reloadPage();


function reloadPage()
{
    $.get('/getInfo', function(data){
        data = $.parseJSON(data);
        curFoodId = data["recipeName"];
        curMovieId = data["movieName"];
        document.getElementById("movieName").innerHTML= data["movieName"];
        document.getElementById("foodName").innerHTML= data["recipeName"];
        document.getElementById("moviePic").src = data["movieImage"];
        document.getElementById("foodPic").src = data["recipeImage"];
    });
}

function sendRate(rate)
{
    var data = {movieId:curMovieId, foodId:curFoodId, rate:rate};
    $.post('/postRate', data, function(){reloadPage()});
}

$('#voteMatch').on('click', function(e) {
    sendRate(1);
});

$('#voteNoMatch').on('click', function(e) {
    sendRate(-1);
});