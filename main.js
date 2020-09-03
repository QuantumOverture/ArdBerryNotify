CurrentID = "Calls";
CurrentIDButton = "cb";
function Calls(){
    document.getElementById(CurrentID).style.display="none";
    document.getElementById(CurrentIDButton).style.color="black";
    CurrentID = "Calls";
    CurrentIDButton = "cb";
    document.getElementById("Calls").style.display="block";
    document.getElementById("cb").style.color="red";
}

function RequestLog(){
    document.getElementById(CurrentID).style.display="none";
    document.getElementById(CurrentIDButton).style.color="black";
    CurrentID = "RequestLog";
    CurrentIDButton = "rlb";
    document.getElementById("RequestLog").style.display="block";
    document.getElementById("rlb").style.color="red";
}

function InternalKey(){
    document.getElementById(CurrentID).style.display="none";
    document.getElementById(CurrentIDButton).style.color="black";
    CurrentID = "InternalKey";
    CurrentIDButton = "ikb";
    document.getElementById("InternalKey").style.display="block";
    document.getElementById("ikb").style.color="red";
}

function InternalInfo(){
    document.getElementById(CurrentID).style.display="none";
    document.getElementById(CurrentIDButton).style.color="black";
    CurrentID = "InternalInfo";
    CurrentIDButton = "iib";
    document.getElementById("InternalInfo").style.display="block";
    document.getElementById("iib").style.color="red";
}


function DataSnapshot(){
    document.getElementById(CurrentID).style.display="none";
    document.getElementById(CurrentIDButton).style.color="black";
    CurrentID = "DataSnapshot";
    CurrentIDButton = "dsb";
    document.getElementById("DataSnapshot").style.display="block";
    document.getElementById("dsb").style.color="red";
}