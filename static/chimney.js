function hide () {
    var x = document.getElementById("pass");
    if (x.type === "password")
    {
         x.type = "text";
    } 
    else 
    {
      x.type = "password";
    }
}
function hidec () {
    var x = document.getElementById("cpass");
    if (x.type === "password")
    {
         x.type = "text";
    } 
    else 
    {
      x.type = "password";
    }
}

function hide_password(){
    let password = document.getElementById("hide") 

    if (password.style.display=='block')
    {
        password.style.display='none';
    }
    else {
        password.style.display='block';
    }
} 


function hide_name(){
    let name = document.getElementById("hide_name")
    if (name.style.display == 'block')
    {
        name.style.display='none';
    }
    else
    {
        name.style.display='block';
    }
    
} 
function hide_email(){
    let email = document.getElementById("hide_email")
    if (email.style.display == 'block')
    {
        email.style.display='none';
    }
    else
    {
        email.style.display='block';
    }
} 
function hide_history(){
    let email = document.getElementById("myTable")
    if (email.style.display == 'block')
    {
        email.style.display='none';
    }
    else
    {
        email.style.display='block';
    }
} 