var socket = io.connect('http://127.0.0.1:5000');

socket.on('connect', function() {
    $.getJSON("https://api.ipify.org?format=json", function(data) {
        const ip = (data.ip)
        const sid = socket.id
        socket.emit('connectx', ip, sid);
    })    
});

window.addEventListener('beforeunload', function(e){
    e.preventDefault()
    socket.emit('disconnectx')
})

const form = document.getElementById('getPlayer')
const signupLink = document.getElementById('signupLink')
const baseUrl = "http://127.0.0.1:5000"

loginButton.addEventListener('click', function(){
    const password = document.getElementById("password").value
    const username = document.getElementById("username").value
    $.getJSON("https://api.ipify.org?format=json", function(data) {
        const ip = (data.ip)
        const sid = socket.id
        socket.emit('login', ip, sid, username, password)
    })
})

socket.on('update state', function(state){
    if (state == "idle"){
        idleState()
    }
})

// $("#content").on("click", "#trotButton", function(){
//     $.get(baseUrl+'/start_trotting')
//     exploreState()
// })

// $("#content").on("click", "#stopTrotButton", function(){
//     $.get(baseUrl+'/stop_trotting')
//     idleState()
// })

socket.on('idle state', function() {
    console.log("now idle")
    idleState()
})

// function exploreState() {
//     console.log("now exploring")
//     $("#content").css("height", "35px")
//     $("#content").css("width", "80px")
//     $('#content').html("<div id='exploreWrapper'>\
//                             <button id='stopTrotButton'>\
//                                 Stop Trotting\
//                             </button>\
//                         </div>") 
// }

function idleState() {
    $("#content").css("height", "35px")
    $("#content").css("width", "80px")
    $('#content').html("<div id='idleWrapper'>\
                            <button id='trotButton'>\
                                Start Trotting\
                            </button>\
                        </div>") 
}