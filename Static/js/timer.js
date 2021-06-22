    console.log("Timer function called");
    var expDate = new Date().getTime();
    
    var countDownDate = expDate + 2401100;
    var x = setInterval(function(){
        console.log("timer function updated");
        var now = new Date().getTime();
        var distance = countDownDate - now;
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
            document.getElementById("timer").innerHTML = minutes + "minutes " + seconds + "seconds ";
            if (distance < 0) {
                clearInterval(x);
             
                document.getElementById("submit_btn").click();
            }
        
            
    },1000);