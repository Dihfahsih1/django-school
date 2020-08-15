$(document).ready(function(){
    $('.collapsible').collapsible();
    $('#btnSearch').click(function () {
        $('.searchWrapper').toggle("slide", {direction:"right"}, 1000);
    })
    $('#searchInput').on("keyup", function () {
        $('.collapsible .collapsible-header.line').each(function () {
            var search= $('#searchInput').val()
            if ($(this).text().search(search) > 0){
                $(this).parent().fadeIn()
            }else{
                $(this).parent().fadeOut()
            }
	    if (search == ""){
                $(this).parent().fadeIn()
            }
        })

    })
});