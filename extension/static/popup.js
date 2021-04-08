var socket = io.connect('http://127.0.0.1:5000');

socket.on('connect', function() {
    $.getJSON("https://api.ipify.org?format=json", function(data) {
        const ip = (data.ip)
        const sid = socket.id
        socket.emit('connection', ip, sid);
    })    
});

socket.on('update state', function(state){
    if (state == "idle") {
        idleState()
    } else if (state == "initialize") {
        initializeState()
    } else if (state == "explore") {
        exploreState()
    } else if (state== "encounter"){
        encounterState()
    }
})

$("#content").on("click", "#loginButton", function(){
    const password = document.getElementById("password").value
    const username = document.getElementById("username").value
    $.getJSON("https://api.ipify.org?format=json", function(data) {
        const ip = (data.ip)
        const sid = socket.id
        socket.emit('login', ip, sid, username, password)
    })
})

$("#content").on("click", "#trotButton", function(){
    $.getJSON("https://api.ipify.org?format=json", function(data) {
        const ip = (data.ip)
        socket.emit('start trotting', ip)
        exploreState()
    })
})


$("#content").on("click", "#stopTrotButton", function(){
    $.getJSON("https://api.ipify.org?format=json", function(data) {
        const ip = (data.ip)
        socket.emit('stop trotting', ip)
        idleState()
    })
})

function encounterState() {
    $("#content").css("height", "450px")
    $("#content").css("width", "600px")
    $("#content").html("<div id='encounterWrapper'>\
                            You're fighting a wild Phox!\
                        </div>")
}

function exploreState() {
    $("#content").css("height", "35px")
    $("#content").css("width", "80px")
    $('#content').html("<div id='exploreWrapper'>\
                            <button id='stopTrotButton'>\
                                Stop Trotting\
                            </button>\
                        </div>") 
}

function idleState() {
    $("#content").css("height", "35px")
    $("#content").css("width", "80px")
    $('#content').html("<div id='idleWrapper'>\
                            <button id='trotButton'>\
                                Start Trotting\
                            </button>\
                        </div>") 
}

function initializeState() {
    $('#content').css("height", "80px")
    $('#content').css("width", "400px")
    $("#content").html('<div id="login">\
                            <form action="" id="getPlayer" method="POST">\
                                <input type="text" id="username" placeholder="Username"/>\
                                <input type="password" id="password" placeholder="Password"/>\
                            </form>\
                            <button id="loginButton">Log In</button>\
                        </div>')
}