var i = 1;
function PysrcTTS(input){
    return  $.ajax({
        type: "POST",
        url: '/student/speakscore',
        async: true,
        data: { 'mydata': input }
    });
}
async function latest_result(){
    
    do {
        try{
            var res = document.getElementById("exam_"+i.toString()).textContent;
            i ++; 
        }
        catch(err){
            //console.log("Attempted = "+attempted);
            break;
        }
    } while(res!=null)
    i--;
    console.log(i);
    res = document.getElementById("marks_"+i.toString()).textContent;
    setTimeout(function(){PysrcTTS("You Scored "+res);},10000);
    //await PysrcTTS("You Scored "+res);
}
latest_result();