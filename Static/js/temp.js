console.log("Running script block static");
var examname = document.getElementById("Examname").textContent;
var examname = document.getElementById("totalquestion").textContent;
var examname = document.getElementById("TotalMarks").textContent;



function runPyScript(input){
    var jqXHR = $.ajax({
        type: "POST",
        url: "/speak",
        async: false,
        data: { mydata: input }
    });

    return jqXHR.responseText;
}
runPyScript(examname);
console.log('Spoke ' + examname);

