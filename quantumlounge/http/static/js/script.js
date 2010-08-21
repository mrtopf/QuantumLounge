/* Author: 

*/

$(document).ready(function () {
    var a=1;
    var tm = TemplateManager();
    tm.render('test', function (d) {
        $("#hans").append(d);
    }, {a: a})
    
    $(".click").live('click',function() {
        a++;
        tm.render('test', function (d) {
            $("#hans").append(d);
        }, {a: a})
        return false;
        
    })
})






















