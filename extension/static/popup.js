const form = document.getElementById('getPlayer')
const signupLink = document.getElementById('signupLink')
const baseUrl = "http://127.0.0.1:5000"

loginButton.addEventListener('click', function(){
    const password = document.getElementById("password").value
    const username = document.getElementById("username").value
    $.post(baseUrl+"/login", {
        username: username,
        password: password
    },
    function(data, status){
        if (data == "success"){
            idleState()
        }
    })
})

function idleState() {
    console.log("you did it")
    $('#content').html('You did it') 
}

// $.get(baseUrl+"/login", function(data){
//     alert($.parseJSON(data))
// })