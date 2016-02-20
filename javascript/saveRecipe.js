



$(document).on("click",".saveRecipe",function() {
//	var urlFromUser = $("[name=url]").val();
	var ingredientList = [];
	$('.ingredient').each(function(i, obj) {
	    ingredientList[i] = $(this).text();
	});
//	alert($(".recipeTitle h1").text());
//	alert("saving");
	var title = $(".recipeTitle h1").text();
	$.ajax({url: "/SaveRecipe",data: {ingredients: JSON.stringify(ingredientList),recipeTitle: title}, success: function(result){
		alert("saved!");
	}});
});