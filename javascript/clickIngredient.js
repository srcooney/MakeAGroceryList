$(document).on("click",".ingredient",function(){
	var parentID = $(this).parent().parent().attr('id');
	if($(this).hasClass("notclicked")){
		var $this = $(this);
		$this.fadeOut( 1000, function(){
			$this.appendTo("#"+parentID+" .used").fadeIn(1000).css("background-color", "#99FF33").addClass("clicked").removeClass("notclicked");
		});
	}
	else{
		var $this = $(this);
		$this.fadeOut( 1000, function(){
			$this.appendTo("#"+parentID+" .notUsed").fadeIn(1000).css("background-color", "#FFFFFF").addClass("notclicked").removeClass("clicked");
		});
	};
});