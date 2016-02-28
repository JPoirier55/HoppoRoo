/**
 * Created by Jake on 2/27/2016.
 */

//function updateFunction(){



    //var interval = setInterval(update, 1000);
    //function update() {
    //    $.ajax({
    //        type: "GET",
    //        url: "http://192.168.42.15?callback=jsonCallBack",
    //        async: false,
    //        jsonpCallback: 'jsonCallBack',
    //        contentType: "application/json",
    //        dataType: 'jsonp',
    //        success: function (json) {
    //            door1 = json['door1'];
    //            door2 = json['door2'];
    //            console.log(door1, door2);
    //        },
    //        error: function(){
    //            console.log('shit');
    //        }
    //    });
    //
    //}


function getData(url, id1, id2) {
        $.get(url, Common.genSafeId(), function(data) {
            $(id1).html(data);
            $(id2).addClass("empty");
            console.log(data);
        });
    }


