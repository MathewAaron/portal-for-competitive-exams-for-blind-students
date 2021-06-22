function PyScriptSTT(){
    $.when($.ajax({
        type: "POST",
        url: '/student/SpeechRecog',
        async: true,
    })).done(function(a1){
        var STTres = a1;
        console.log("Speech Received = " + STTres);
        return STTres;
    });

    
}