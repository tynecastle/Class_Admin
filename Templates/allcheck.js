(function() {
    //$('#body').allcheck();
    jQuery.fn.extend({
        allcheck:function(){
            //$(this) == $('#body')
            $(this).find(':checkbox').each(function(){
                this.checked = true;
            });
        },
        uncheck:function(){
            $(this).find(':checkbox').each(function(){
                this.checked = false;
            });
        }
    });
    
    //$.allcheck()
    jQuery.extend({
        jallcheck:function(arg){
            $(arg).find(':checkbox').attr('checked',true)
        },
        juncheck:function(arg){
            $(arg).find(':checkbox').attr('checked',false)
        }
    });
})();