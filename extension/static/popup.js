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

socket.on('draw details', function(infoDict) {
    drawCombatDetails(infoDict)
})

socket.on('generate attack menu', function(attacks){
    console.log(attacks)
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

$("#content").on("click", ".attack", function() {
    const sid = socket.id
    socket.emit('get attack menu', sid)
})

// General handlers for each new state.
// Typically called when the popup is reopened
// Also called when switching between explore and idle states

function encounterState() {
    $("#content").css("height", "450px")
    $("#content").css("width", "600px")
    $("#content").html("<div id='encounterWrapper'>\
                            Getting information to display combat...\
                        </div>")
    renderEncounter()
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

// Combat display
// Top level combat function for drawing combat
function renderEncounter() {
    drawGeneralCombatBlueprint()
    drawDetailCombatBlueprint()
    drawCombatButtons()
    getInfoFromServer()
    // getInfoFromServer() calls drawCombatDetails(infoDict)
}

// Render the outline and divs for combat
function drawGeneralCombatBlueprint() {
    $('#content').html("<div id='encounterWrapper'>\
                            <div id='enemyInfo'></div>\
                            <div id='enemyArt'>enemy art</div>\
                            <div id='playerArt'>player art</div>\
                            <div id='playerInfo'></div>\
                            <div id='info'></div>\
                        </div>") 
}

//Put different divs in place to hold specific info bits for combat
function drawDetailCombatBlueprint(){
    $("#enemyInfo").append("<div class='name'>name and level</div>")
    $("#enemyInfo").append("<div class='health'>health</div>")
    $("#enemyInfo").append("<div class='ram'>RAM</div>")
    $("#enemyInfo").append("<div class='status'></div>")
    $("#playerInfo").append("<div class='name'>name and level</div>")
    $("#playerInfo").append("<div class='health'>health</div>")
    $("#playerInfo").append("<div class='ram'>RAM</div>")
    $("#playerInfo").append("<div class='status'></div>")
}

function drawCombatButtons(){
    $("#info").append("<div class='run btn'>Run</div>")
    $("#info").append("<div class='swap btn'>Swap</div>")
    $("#info").append("<div class='attack btn'>Attack</div>")
}

function drawCombatDetails(infoDict) {
    const wildPhoxMaxHP = infoDict["wild_phox_max_hp"]
    const wildPhoxCurrentHP = infoDict["wild_phox_current_hp"]
    const wildPhoxMaxRAM = infoDict["wild_phox_max_RAM"]
    const wildPhoxCurrentRAM = infoDict["wild_phox_current_RAM"]
    const wildPhoxName = infoDict["wild_phox_name"]
    const wildPhoxLevel = infoDict["wild_phox_level"]
    const wildPhoxStatus = infoDict["wild_phox_status"]
    drawWildPhox(wildPhoxMaxHP, wildPhoxCurrentHP, wildPhoxMaxRAM, wildPhoxCurrentRAM, wildPhoxName, wildPhoxLevel, wildPhoxStatus)
    const phoxMaxHP = infoDict["phox_max_hp"]
    const phoxCurrentHP = infoDict["phox_current_hp"]
    const phoxMaxRAM = infoDict["phox_max_RAM"]
    const phoxCurrentRAM = infoDict["phox_current_RAM"]
    const phoxName = infoDict["phox_name"]
    const phoxLevel = infoDict["phox_level"]
    const phoxStatus = infoDict["phox_status"]
    drawPhox(phoxMaxHP, phoxCurrentHP, phoxMaxRAM, phoxCurrentRAM, phoxName, phoxLevel, phoxStatus)
}

function drawWildPhox(maxhp, hp, maxram, ram, pname, lvl, status) {
    var nameInfo = document.querySelectorAll("#enemyInfo .name")
    nameInfo[0].innerHTML = "Level "+lvl+ " "+pname
    var healthInfo = document.querySelectorAll("#enemyInfo .health")
    healthInfo[0].innerHTML = "Health: "+hp+"/"+maxhp
    var ramInfo = document.querySelectorAll("#enemyInfo .ram")
    ramInfo[0].innerHTML = "RAM: "+ram+"/"+maxram
    var statusInfo = document.querySelectorAll("#enemyInfo .status")
    if (status == true){
        statusInfo[0].innerHTML = "Status: "+status
    }
}

function drawPhox(maxhp, hp, maxram, ram, pname, lvl, status){
    var nameInfo = document.querySelectorAll("#playerInfo .name")
    nameInfo[0].innerHTML = "Level "+lvl+ " "+pname
    var healthInfo = document.querySelectorAll("#playerInfo .health")
    healthInfo[0].innerHTML = "Health: "+hp+"/"+maxhp
    var ramInfo = document.querySelectorAll("#playerInfo .ram")
    ramInfo[0].innerHTML = "RAM: "+ram+"/"+maxram
    var statusInfo = document.querySelectorAll("#playerInfo .status")
    if (status == true){
        statusInfo[0].innerHTML = "Status: "+status
    }
}

function getInfoFromServer() {
    $.getJSON("https://api.ipify.org?format=json", function(data) {
        const ip = (data.ip)
        const sid = socket.id
        socket.emit('start combat', ip, sid)
    })
}