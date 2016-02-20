
var genericRecipe = '<div class="col-md-10 genericRecipe">' +
'<div class="col-md-10 recipeTitle" ><h1 id="context" data-toggle="context" data-target="#context-menu"></h1></div>' +
'<div class="saveRecipe" ><span class="glyphicon glyphicon-leaf" aria-hidden="true"></span></div>' +
'<div class="deleteRecipe" ><span class="glyphicon glyphicon-fire" aria-hidden="true"></span></div>' +
'<div class="col-md-5 notUsed"></div>'+
'<div class="col-md-5 used"></div>'+
'</div>';

var contextmenu = '<div class="savebt" id="context-menu">'+
'<ul class="dropdown-menu savebt" role="menu">'+
'<li class="savebt"><a class="savebt" tabindex="-1" href="#">Save</a></li>'+
'<li><a tabindex="-1" href="#">Delete</a></li>'+
'</ul>'+
'</div>';

$(document).ready(function(){
$('body').append(contextmenu);
 });
var recipeCount=0;
$(document).on("click","#submitbt",function() {
	var urlFromUser = $("[name=url]").val();
	$.ajax({url: "/GetIngredients",data: {url: urlFromUser}, success: function(result){
		ingredientsJson = JSON.parse(result);
		var recipeID = "Recipe" + recipeCount.toString();

		$( ".recipelist" ).append(genericRecipe);
		var thisRecipe = $(".genericRecipe");
		thisRecipe.removeClass("genericRecipe");
		$(thisRecipe).attr('id',recipeID);
		$(".recipeTitle").find("h1").text(recipeID);
		$('.context').contextmenu();
		for (i=0;i < ingredientsJson.ingredientsList.length;i+=1) {

			var ingredient = document.createElement( "div" );
			$("#" + recipeID +" .notUsed").append('<div class="form-control ingredient notclicked">'
					+ ingredientsJson.ingredientsList[i]+'<span class="glyphicon glyphicon-remove pull-right deleteIngredient"></span></div>');
			$(ingredient).addClass("form-control ingredient notclicked");
		};

		recipeCount +=1;
	}});
});

$(document).on("click",".deleteIngredient",function() {
	$(this).parent().animate({
	    backgroundColor: "#aa0000",
	  }, 1000, function() {
		  $(this).remove();
	    // Animation complete.
	  });
	
	
});