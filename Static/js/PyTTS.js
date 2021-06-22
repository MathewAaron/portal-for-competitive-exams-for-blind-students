function PyScriptTTS(input){
    var TTSres = $.when($.ajax({
        type: "POST",
        url: '/student/speak',
        async: true,
        data: { 'mydata': input }
    })).done(function(a1){
        var TTSres = a1;
        console.log("Spoke = " + TTSres);
        return TTSres;

    });

    
}