$(function () {
	$('#foot-text').append('&copy; ' + new Date().getFullYear());
	
	$("img.pic-next-text")
		.mouseover(function() { 
			$(this).attr("src", "static/imgs/icons/metroicons/back_hover.png");
		})
		.mouseout(function() {
			$(this).attr("src", "static/imgs/icons/metroicons/back.png");
		});
		
	$("img.pic-next-text-one-level")
		.mouseover(function() { 
			$(this).attr("src", "../static/imgs/icons/metroicons/back_hover.png");
		})
		.mouseout(function() {
			$(this).attr("src", "../static/imgs/icons/metroicons/back.png");
		});
});