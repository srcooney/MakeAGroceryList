$(document).ready(function() {
	$.ajax({url: "/GetSavedRecipes", success: function(result){
		recipeJson = JSON.parse(result);
		for (i=0;i < recipeJson.recipeList.length;i+=1) {
			$(".savedRecipeList").append('<div class="form-control" style="text-align: center;">'+ recipeJson.recipeList[i].title+'</div>');
		};
	}});
});