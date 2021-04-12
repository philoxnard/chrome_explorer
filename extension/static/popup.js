var socket = io.connect('http://127.0.0.1:5000');
var globalAttacks = []

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
    } else if (state == "encounter" || state == "initialize encounter"){
        encounterState(state)
    }
})

socket.on('draw details', function(infoDict) {
    drawCombatDetails(infoDict)
})

socket.on('generate attack menu', function(attacks){
    $("#info").append("<div id='attackMenu'></div>")
    $("#attackMenu").html("")
    globalAttacks = attacks
    for (i=0; i<globalAttacks.length; i++){
        $("#attackMenu").append("<div class='attackOption'>"+globalAttacks[i]["name"]+"</div>")
    }
})

socket.on('update readout', function(readout) {
    console.log('attempting to update readout')
    $(".readout").html(readout["ownership"]+" "+readout["attacker"]+" used " +readout["attack"]+".")
    $(".readout").append("<br>It dealt "+readout["damage"]+" damage.")
    $(".readout").append("<div class='nextTurn btn'>Continue</div>")
})

$("#content").on('mouseover', '.attackOption', function(){
    for (i=0; i<globalAttacks.length; i++){
        if (this.innerHTML == globalAttacks[i]["name"]){
            let atk = globalAttacks[i]
            $("#info").append("<div id='tooltip'></div>")
            $("#tooltip").html("Damage: "+atk["damage"]+"<br> \
                                Cost: "+atk["cost"]+"<br> \
                                Family: "+atk["family"]+"<br> \
                                Style: "+atk["style"]+"<br> \
                                "+atk["effect"])
        }
    }
})

$("#content").on('mouseout', '.attackOption', function(){
    $("#tooltip").remove()
})

$("#content").on('click', '.attackOption', function(){
    let attackName = this.innerHTML
    let sid = socket.id
    console.log(attackName)
    socket.emit('click attack', attackName, sid)
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

$("#content").on("click", ".accept", function() {
    $.getJSON("https://api.ipify.org?format=json", function(data) {
        const ip = (data.ip)
        const sid = socket.id
        socket.emit('combat loop', ip, sid)
    })
})

$("#content").on("click", ".decline", function() {
    $.getJSON("https://api.ipify.org?format=json", function(data) {
        const ip = (data.ip)
        socket.emit('start trotting', ip)
        exploreState()
    })
})

// General handlers for each new state.
// Typically called when the popup is reopened
// Also called when switching between explore and idle states

function encounterState(state) {
    $("#content").css("height", "450px")
    $("#content").css("width", "600px")
    $("#content").html("<div id='encounterWrapper'>\
                            Getting information to display combat...\
                        </div>")
    renderEncounter()
    if (state == "initialize encounter") {
        initializeEncounter()
    } else if (state == "encounter")
    {
        const sid = socket.id
        socket.emit('get attack menu', sid)
    }
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

// Display when the state is initializing encounter
function initializeEncounter() {
    $('#info').html("")
    $("#info").append("<div class='decline btn'>Run</div>")
    $("#info").append("<div class='accept btn'>Battle</div>")
}

// Combat display
// Top level combat function for drawing combat
function renderEncounter() {
    drawGeneralCombatBlueprint()
    drawDetailCombatBlueprint()
    drawCombatButtons()
    getInfoFromServer()
    getTurnInfo()
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
    $("#enemyInfo").append("<div class='name'></div>")
    $("#enemyInfo").append("<div class='health'></div>")
    $("#enemyInfo").append("<div class='ram'></div>")
    $("#enemyInfo").append("<div class='status'></div>")
    $("#playerInfo").append("<div class='name'></div>")
    $("#playerInfo").append("<div class='health'></div>")
    $("#playerInfo").append("<div class='ram'></div>")
    $("#playerInfo").append("<div class='status'></div>")
}

function drawCombatButtons(){
    $('#info').html('')
    $("#info").append("<div class='run btn'>Run</div>")
    $("#info").append("<div class='swap btn'>Swap</div>")
    $("#info").append("<div class='readout'></div>")
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
        socket.emit('initialize encounter state', ip, sid)
    })
}

// Tells the client if its your turn, or tells you what the opponent did on its turn
function getTurnInfo() {
    const sid = socket.id
    socket.emit('get turn info', sid)
}