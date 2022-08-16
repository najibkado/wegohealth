
$(".chosen-select").chosen({
    no_results_text: "Oops, nothing found!"
})


$(function(){ 
$("#form").submit(function(e){ 
    e.preventDefault(); 
    $.ajax({ 
        url:'email.php', 
        type:'POST', 
        data:$("#form").serialize(), 
        success:function(e) { 
        } 
    }); 
}); 
}); 