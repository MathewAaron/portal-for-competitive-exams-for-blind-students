//console.log("Running script block static");
function PyScriptSTT(){
    return $.ajax({
        type: "POST",
        url: '/student/SpeechRecog',
        async: true,
    });
}

function PyScriptTTS(input){
    return  $.ajax({
        type: "POST",
        url: '/student/speak',
        async: true,
        data: { 'mydata': input }
    });
}
async function Read_Instructions(){
    var examname = document.getElementById("Examname").textContent;
    var totalq = document.getElementById("totalquestion").textContent;
    var totalm = document.getElementById("TotalMarks").textContent;
    $.when(PyScriptTTS(examname)).done(function(a1){
        $.when(PyScriptTTS(totalq)).done(function(a2){
            $.when(PyScriptTTS(totalm)).done(function(a3){
                var ins = "instruct";
                var i= 1;
                var text = "";
                do{
                    try {
                        var instruct = document.getElementById(ins.concat(i.toString())).textContent;
                        //console.log("Instruction = " + ins.concat(i.toString()));
                        if (instruct!=null){
                            text = text + instruct;
                        }
                        i=i+1;
                        //console.log(text);
                    }
                    catch(err) {
                        break;
                    }
                } while (instruct!=null)
                $.when(PyScriptTTS(text)).done(function(a4){
                    console.log("instructions complete");
                    start_exam();
                });
            });
        });
    });
}
function instruction(){
    var text = "To listen to Instructions say instructions";
    $.when(PyScriptTTS(text)).done(function(a5){
        var flag = 0;
        $.when(PyScriptSTT()).done(function(s1){  
            var speechResult = s1;
            if(speechResult == "instructions" || speechResult == "instruction") {
                flag = 1;
                //console.log("speech result: "+speechResult);
                //Reading Exam Instructions
                Read_Instructions();
            }
            else{
                flag = 2;
                console.log("speech result: "+speechResult+"No such operation");
                var text = "No such operation";
                $.when(PyScriptTTS(text)).done(function(a1){
                    instruction();
                });
                
            }

        });
    });            
}
function start_exam(){
    var st_exam_text = "To listen to instructions again say Instructions or Say start to start the exam";
    $.when(PyScriptTTS(st_exam_text)).done(function(a1){
        $.when(PyScriptSTT()).done(function(s2){
            console.log("a2 = " + s2);
            var speechResult = s2;
            if(speechResult == "start" || speechResult == "start exam"){
                document.getElementById("start_exam_button").click();
            }
            else if (speechResult == "instructions" || speechResult == "instruction"){
                    Read_Instructions();
                }
            else{
                console.log("speech result: "+speechResult+"\t No such operation");
                var text = "No such operation";
                PyScriptTTS(text);
                start_exam();
                
            }
    
        });
    });
    
}

$(document).ready(function(){
instruction();
//start_exam();
});