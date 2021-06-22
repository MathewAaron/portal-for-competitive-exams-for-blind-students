var i = 1, k, attempted = 1,distance;


function PysrcSTT(){
    console.log("STT");
    return $.ajax({
        type: "POST",
        url: '/student/SpeechRecog',
        async: true,
    });
}
function PysrcTTS(input){
    return  $.ajax({
        type: "POST",
        url: '/student/speak',
        async: true,
        data: { 'mydata': input }
    });
}


async function speaktimer(){
    dist = distance - 5000;
    var minutes = Math.floor(dist  / (1000 * 60));
    var seconds = Math.floor((dist % (1000 * 60)) / 1000);
    await PysrcTTS("Time Remaining is" + minutes+ " Minutes " + seconds+ " seconds ");
}


async function No_Question(){
    console.log(attempted);
    do {
        try{
            var Qphrase = document.getElementById("question_phrase"+attempted.toString()).textContent;
            attempted ++; 
        }
        catch(err){
            //console.log("Attempted = "+attempted);
            break;
        }
    } while(Qphrase!=null)
    attempted --;
    console.log("Total Questions = "+ attempted);
}

async function timer(){
   
    //console.log(typeof time_min);
    var expDate = new Date().getTime();
    //console.log(expDate)
    var countDownDate = expDate + (time_min)*60*1000;
    //console.log(countDownDate);
    
    var x = setInterval(function(){
        //console.log("timer function updated");
        var now = new Date().getTime();
        distance = countDownDate - now;
        var minutes = Math.floor(distance  / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
            document.getElementById("Timer").innerHTML = minutes + " minutes " + seconds + " seconds ";
            if (distance < 0) {
                clearInterval(x);
                document.getElementById("submit_btn").click();
            }  
    },1000);
}

function opselect(){
    return $.ajax({
        type: "POST",
        url: '/student/optionselect',
        async: true,
    });
}

async function Read_Question(){
        console.log(i);
        try {
            if(i<=0){
                console.log("This is the first question");//TTS
                await PysrcTTS("This is the first question");
                i=1;
            }
            var qphrase = document.getElementById("question_phrase"+i.toString()).textContent;
            var Qphrase = "Question " + qphrase;
            if (Qphrase!=null){
                var a = await PysrcTTS(Qphrase);
                console.log(a);
                await Read_Options(i);
            }    
        }
        catch(err) {
            console.log("Last Question");
            await PysrcTTS("That was the last question. Do you want to check review questions");
            var ch = await PysrcSTT();
            console.log('ch = '+ch);
            if (ch == "review questions"||ch == "review question"||ch == "review"){
                await Review_Q();
            }else{
                await navig();
            }
        }

}

async function Review_Q(){
    console.log("Review Q")
    if (review.length == 0){
        console.log("No review questions");
        await PysrcTTS("No review questions. Say submit to submit the test");
        navig();
    }else{
        for(k=0;k<review.length;k++){
            var temp = review[k];
            var rphrase = document.getElementById("question_phrase"+temp.toString()).textContent;
            var Rphrase = "Question " + rphrase;
            console.log("K = "+k);
            if (Rphrase!=null){
                var a = await PysrcTTS(Rphrase);
                console.log("temp = "+temp);
                await Read_Options(temp);
                await Rnavig();
            }
        }
        if (k==review.length){
            await PysrcTTS("All questions have been reviewed");
            var navi = await PysrcSTT();
            console.log("navi = "+navi);
            if (navi == "Submit" ||navi == "submit"){
                //check if all questions are attempted
                document.getElementById("submit_btn").click();
                await PysrcTTS("Submitting Test");
            }else{
                navig();
            }
        }
    }
}

async function Rnavig(){
    var x = await PysrcTTS("Say next question to load the next review question, Say previous question to answer the previous review question, Say submit to submit the Test");
    var navi = await PysrcSTT();
    console.log("navi = "+navi);
    if (navi == "Submit" ||navi == "submit"){

        document.getElementById("submit_btn").click();
        await PysrcTTS("Submitting Test");
    }else if (navi == "next question"){
        //k=k+1;
        //Review_Q();
    }else if (navi == "previous question"){
        k=k-2;
        if (k<0){
            await PysrcTTS("This is the first Review Question");
            k=0;
        }
        //exam_nav();
    }else if (navi == "time"|| navi == "time "||navi == " time "||navi == " time"){
        await speaktimer();
        await Rnavig();
        
    }else{
        await PysrcTTS("Invalid Navigation");
        await Rnavig();
    }
}

async function Read_Options(index){
    console.log("Read options" + index);
    var j;
    for (j = 1; j < 5; j++) {
        try{
            var option = document.getElementById("option"+j.toString()+"_"+index.toString()).textContent;
            var Option = "Option "+ j.toString()+".."+option.toString()+".";
            if (Option!=null){
                var a = await PysrcTTS(Option);
                console.log(Option);
            }     
        }
        catch(err) {
            console.log("Option out of index was null");
        }     
    }
    await ans_ques(index);
}

async function ans_ques(index){
    console.log("Answer question");
    var Ans = await PysrcSTT();
    //$.when(PysrcSTT()).done(function(Ans){
        console.log(Ans);
        if (Ans == "Answer" ||Ans == "Answers"||Ans == "answers"||Ans == "answer"){
            console.log("BEEP");
            await PysrcTTS("Beep");                
            //var opchoice = 0;
            var opchoice = await opselect();
            console.log(opchoice);
                if (opchoice!= null){
                    var Opch =  opchoice;
                    //console.log(Opch);
                    if(Opch == "Option1"|| Opch == "option 1"|| Opch == "option one"|| Opch == "Option one "|| Opch == "one"||Opch == "1" ){
                        radios = document.getElementsByName(index);
                        radios[0].checked = "true";
                        var op = document.getElementById("option1_"+index.toString()).innerHTML;
                        console.log("Selected Option 1 : "+op);
                        await PysrcTTS("Selected Option 1 : "+op);    
                    }else if (Opch == "Option2"|| Opch == "option 2"|| Opch == "option two"|| Opch == "two"|| Opch == "2" ){
                        radios = document.getElementsByName(index);
                        radios[1].checked = "true";
                        var op = document.getElementById("option2_"+index.toString()).innerHTML;
                        await PysrcTTS("Selected Option 2 : "+op);
                        
                    }else if (Opch == "Option3"|| Opch == "option 3"|| Opch == "option three"|| Opch == "three"|| Opch == "3" ){
                        
                        radios = document.getElementsByName(index);
                        radios[2].checked = "true";
                        var op = document.getElementById("option3_"+index.toString()).innerHTML;
                        await PysrcTTS("Selected Option 3 : "+op);  
                        
                    }else if (Opch == "Option4"|| Opch == "option 4"|| Opch == "option four"|| Opch == "four"|| Opch == "4" ){
                        
                        radios = document.getElementsByName(index);    
                        radios[3].checked = "true";
                        var op = document.getElementById("option4_"+index.toString()).innerHTML;
                        await PysrcTTS("Selected Option 4 : "+op);
                        
                    }else{
                        await PysrcTTS(Opch+" is an invalid option choice");
                        await PysrcTTS("Say Answer then the Option name to answer the question");
                        await ans_ques();
                    }
                    console.log("Option Received = " + Opch);
                }
                else{
                    await PysrcTTS("Please repeat the answer");
                    await ans_ques(index);    
                }
        } else{
            await PysrcTTS("Say Answer then the Option name to answer the question");
            await ans_ques(index);
        }
}

async function navig(){
    var x = await PysrcTTS("Say Next question to load the next question, Say previous question to answer the previous question, Say submit to submit the Test");
    var navi = await PysrcSTT();
    console.log("navi = "+navi);
    if (navi == "Submit" ||navi == "submit"){
        if (i<=attempted){
            await PysrcTTS("Not all Questions have been attempted. Say Submit to confirm submission of the test.");
            var confirm = await PysrcSTT();
            console.log("Confirm = "+confirm);
            if (confirm == "Submit" || confirm == "submit"){
                await PysrcTTS("Submitting Test");
                document.getElementById("submit_btn").click();
            }else{
                navig();
            }
        }else{
            await PysrcTTS("Submitting Test");
            document.getElementById("submit_btn").click();
        }
    }else if (navi == "next question"){
        i=i+1;
        exam_nav();
    }else if (navi == "previous question"){
        i=i-1;
        exam_nav();
    }else if (navi == "time"|| navi == "time "||navi == " time "||navi == " time"){
        await speaktimer();
        navig();
        
    }else if (navi == "mark for review"){
        await PysrcTTS("Question Marked for review");
        review.push(i);
        console.log("Review = " + review)
        navig();
    }else{
        await PysrcTTS("Invalid Navigation");
        navig();
    }
}
async function question_flow(){
    //Read the question
    await Read_Question();
    console.log("Read Question Complete");
    //Ask for navigation options (Next/prev)
    navig();
    
}

async function exam_nav(){

    question_flow(); //To Read Question and Corresponding Options
    console.log("flow completed i = "+i.toString());

}
var review = [];
$(document).ready(function(){
timer();
//speaktimer();
No_Question();
//timer();
exam_nav();
});