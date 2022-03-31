window.addEventListener("load", () => {
    let long;
    let lat;
    
    if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(positon => {
            latitude = positon.coords.latitude;
            longitude = positon.coords.longitude;

            const myapi = 'https://api.openweathermap.org/data/2.5/weather?lat=' + latitude +'&lon=' + longitude + '&units=metric&appid=f7b68313fbadbfd6e421a1e73730d7cc';
            
            fetch(myapi)
            .then(response => {
            return response.json();
            })
            .then(data => {
            console.log(data);

            $('.temp').text(Math.round(data.main.temp));
            //$('.location').text(data.name);
            $('.hum').text(data.main.humidity);
            $('.weatherIcon').attr('src', 'http://openweathermap.org/img/w/' + data.weather[0].icon + '.png ');
            
            switch(data.weather[0].main) {
                case 'Clear':
                    $('weatherIcon').css('background-image', 'url(Sunny.jpg)');
                    $('.weather').text("晴れ");
                    break;
                case 'Rain':
                    $('weatherIcon').css('background-image', 'url(Rain.jpg)');
                    $('.weather').text("雨");
                    break;
                case 'Clouds':
                    $('weatherIcon').css('background-image', 'url(Cloudy.jpg)');
                    $('.weather').text("くもり");
                    break;
                case 'Snow':
                    $('weatherIcon').css('background-image', 'url(Snowy.jpg)');
                    $('.weather').text("雪");
                    break;
                default:
                    $("weatherIcon").text("<img src='http://openweathermap.org/img/w/01n.png' >");
            }
            });
        });
    }else{
        alert("あなたの端末では、位置情報を取得できません。")
    }
});

//https://api.openweathermap.org/data/2.5/weather?lat=35&lon=139&appid={API key}

//f7b68313fbadbfd6e421a1e73730d7cc

//AIzaSyCcPtf5s40aXHXxBCv6vbQVzMDRa1JvX4I
