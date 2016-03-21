/**
 * Created by Jake on 2/27/2016.
 */

var interval = setInterval(queue, 1000);
console.log(interval);

function queue(){
    update("192.168.42.15");
}
function update(ip) {
    $.ajax({
        type: "GET",
        url: "http://" + ip +"?callback=jsonCallBack",
        async: false,
        jsonpCallback: 'jsonCallBack',
        contentType: "application/json",
        dataType: 'jsonp',
        success: function (json) {
            console.log(json);
        },
        error: function(){
            console.log('shit');
        }
    });
}

function toggle(){
    console.log(clearInterval(interval));
    console.log(interval);
}




