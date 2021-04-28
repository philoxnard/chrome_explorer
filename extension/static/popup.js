// var socket = io.connect('http://18.222.237.192:8000'); //host for AWS server
var socket = io.connect('http://127.0.0.1:5000'); // host for local test server
var globalAttacks = []
var globalData = []
var globalPhox = null

socket.on('connect', function() {
    // $.getJSON("https://api.ipify.org?format=json", function(data) {
    //     const ip = (data.ip)
    const sid = socket.id
    socket.emit('connection', sid);
    // })    
});

socket.on('disconnect', function() {
    const sid = socket.id
    socket.emit('disconnection', sid)
})

socket.on('update state', function(state){
    if (state == "idle") {
        idleState()
    } else if (state == "initialize") {
        initializeState()
    } else if (state == "explore") {
        exploreState()
    } else if (state.includes("encounter")){
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
    $(".readout").html(readout["ownership"]+" "+readout["attacker"]+" used " +readout["attack"]+".")
    if (readout["clash"]) {
        $(".readout").append("  "+readout["clash"])
    }
    if (readout["pre effect"]) {
        $(".readout").append("<br>"+readout["pre effect"])
    }
    $(".readout").append("<br>It dealt "+readout["damage"]+" damage.")
    if (readout["post effect"]) {
        $(".readout").append("<br>"+readout["post effect"])
    }
    if (readout["swap needed"]) {
        $(".readout").append("<br>"+readout["swap needed"])
    } else {
    $(".readout").append("<div class='nextTurn btn'>Continue</div>")
    }
})

socket.on('swapped phox', function(phox) {
    encounterState("encounter")
    $(".readout").html("Go get 'em, "+phox+"!!")
    $(".readout").append("<div class='nextTurn btn'>Continue</div>")
})

socket.on('your turn readout', function(){
    $(".readout").html("It's your turn!")
})

socket.on('display cleanup', function(info_dict){
    $('.readout').html('Your '+info_dict["phox"]+ " gained "+info_dict["experience"]+" experience!")
    if (info_dict["level"]){
        $('.readout').append('<br>'+info_dict["phox"]+" grew to level "+info_dict["level"]+"!")
        $('.readout').append('<br>Go to phoxtrot.com to select your new upgrade!')
    }
    if (info_dict["newPhox"]){
        $('.readout').append('<br>Congratulations! You added '+info_dict["newPhox"]+' to your collection!')
        $('.readout').append('<br>Go to phoxtrot.com to add it to your party!')
    }
    $('.readout').append('<br>Click "Run" to continue trotting.')
})

socket.on('draw party', function(data){
    globalData = data
    drawParty(data)
})

socket.on('draw collection', function(collection){
    drawCollection(collection)
})

socket.on('view phox', function(phoxSpecies){
    displayPhox(phoxSpecies)
})

socket.on('display reset upgrades', function(){
    globalPhox["upgrade indexes"] = []
    drawUpgradeTree(globalPhox["upgrade tree"])
})

socket.on('update upgrades', function(new_indexes){
    globalPhox["upgrade indexes"] = new_indexes
    drawUpgradeTree(globalPhox["upgrade tree"])
})

socket.on('callback view party', function(){
    const sid = socket.id
    socket.emit('view party', sid)
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

// Used while viewing a Phox in the menu
$("#content").on('mouseover', '.attack', function(){
    for (i=0; i<globalAttacks.length; i++){
        if (this.innerHTML == globalAttacks[i]["name"]){
            let atk = globalAttacks[i]
            $("#content").append("<div id='tooltipViewPhox'></div>")
            $("#tooltipViewPhox").html("Damage: "+atk["damage"]+"<br> \
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

$("#content").on('mouseout', '.attack', function(){
    $("#tooltipViewPhox").remove()
})

$("#content").on('click', '.attackOption', function(){
    let attackName = this.innerHTML
    let sid = socket.id
    socket.emit('click attack', attackName, sid)
})

$("#content").on("click", "#loginButton", function(){
    const password = document.getElementById("password").value
    const username = document.getElementById("username").value
    // $.getJSON("https://api.ipify.org?format=json", function(data) {
    //     const ip = (data.ip)
    const sid = socket.id
    socket.emit('login', sid, username, password)
    // })
})

$("#content").on("click", "#trotButton", function(){
    // $.getJSON("https://api.ipify.org?format=json", function(data) {
    //     const ip = (data.ip)
    socket.emit('start trotting')
    exploreState()
    // })
})


$("#content").on("click", "#stopTrotButton", function(){
    // $.getJSON("https://api.ipify.org?format=json", function(data) {
    //     const ip = (data.ip)
    socket.emit('stop trotting')
    idleState()
    // })
})

$("#content").on("click", ".accept", function() {
    // $.getJSON("https://api.ipify.org?format=json", function(data) {
    //     const ip = (data.ip)
    const sid = socket.id
    socket.emit('combat loop', sid)
    // })
})

$("#content").on("click", ".nextTurn", function() {
    // $.getJSON("https://api.ipify.org?format=json", function(data) {
    //     const ip = (data.ip)
    const sid = socket.id
    socket.emit('combat loop', sid)
    // })
})

$("#content").on("click", ".decline", function() {
    // $.getJSON("https://api.ipify.org?format=json", function(data) {
    //     const ip = (data.ip)
    socket.emit('start trotting')
    exploreState()
    // })
})

$("#content").on("click", ".run", function() {
    // $.getJSON("https://api.ipify.org?format=json", function(data) {
    //     const ip = (data.ip)
    socket.emit('start trotting')
    exploreState()
    // })
})

$("#content").on('click', '.swap', function(){
    const sid = socket.id
    socket.emit('view party', sid)
})

$("#content").on('click', "#viewParty", function(){
    const sid = socket.id
    socket.emit('view party', sid)
})

$("#content").on('click', '.phox', function(){
    let raw_phox = this.innerHTML
    let sid = socket.id
    socket.emit('select phox', raw_phox, sid)
})

$("#content").on('click', '#viewUpgrades', function(){
    $("#content").css("height", "450px")
    $("#content").css("width", "600px")
    $("#content").html("")
    drawUpgradeMenu()
})

$('#content').on('click', '.upgrade', function(){
    const splitParent = this.parentElement.className.split(" ")
    const row = splitParent[1]
    const rowIndex = row.substring(3)
    const splitSelf = this.className.split(" ")
    const option = splitSelf[1]
    const optionIndex = option.substring(6)
    const sid = socket.id
    const species = globalPhox["species"]
    socket.emit('select upgrade', species, rowIndex, optionIndex, sid)
    $("#upgradeTooltip").remove()
})

$("#content").on('mouseover', '.upgrade', function(){
    const baseUpgrades = globalPhox["base upgrades"]
    const upgradeTree = globalPhox["upgrade tree"]
    const upgradeTreeUpgrades = []
    for (i=0; i<upgradeTree.length; i++){
        for (n=0; n<upgradeTree[i].length; n++){
            upgradeTreeUpgrades.push(upgradeTree[i][n])
        }
    }
    const upgrades = baseUpgrades.concat(upgradeTreeUpgrades)
    console.log(upgrades)
    for (i=0; i<upgrades.length; i++) {
        if (this.innerHTML == upgrades[i]["name"]) {
            $("#content").append("<div id='upgradeTooltip'></div>")
            $("#upgradeTooltip").html(upgrades[i]["effect"])
        }
    }
})

$("#content").on('mouseout', '.upgrade', function(){
    $("#upgradeTooltip").remove()
})

$("#content").on('click', '#resetUpgrades', function(){
    const sid = socket.id
    socket.emit('reset upgrades', globalPhox["species"], sid)
})

$("#content").on('click', '.collectionPhox', function(){
    const phox = this.innerHTML
    const sid = socket.id
    socket.emit('swap collection', phox, sid)
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
    else if (state == "encounter cleanup"){
        const sid = socket.id
        socket.emit('get cleanup info', sid)
    }
}

function exploreState() {
    $("#content").css("height", "75px")
    $("#content").css("width", "80px")
    $('#content').html("<div id='exploreWrapper'>\
                            <button id='stopTrotButton'>\
                                Stop Trotting\
                            </button>\
                        </div>") 
    drawPartyButton()
}

function idleState() {
    $("#content").css("height", "75px")
    $("#content").css("width", "80px")
    $('#content').html("<div id='idleWrapper'>\
                            <button id='trotButton'>\
                                Start Trotting\
                            </button>\
                        </div>") 
    drawPartyButton()
}

function initializeState() {
    $('#content').css("height", "60px")
    $('#content').css("width", "400px")
    $("#content").html('<div id="login">\
                            <form action="" id="getPlayer" method="POST">\
                                <input type="text" id="username" placeholder="Username"/>\
                                <input type="password" id="password" placeholder="Password"/>\
                            </form><br>\
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
                            <div id='enemyArt'></div>\
                            <div id='playerArt'></div>\
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
    const wildPhoxArt = infoDict["wild_phox_art"]
    drawWildPhox(wildPhoxMaxHP, wildPhoxCurrentHP, wildPhoxMaxRAM, wildPhoxCurrentRAM, wildPhoxName, wildPhoxLevel, wildPhoxStatus, wildPhoxArt)
    const phoxMaxHP = infoDict["phox_max_hp"]
    const phoxCurrentHP = infoDict["phox_current_hp"]
    const phoxMaxRAM = infoDict["phox_max_RAM"]
    const phoxCurrentRAM = infoDict["phox_current_RAM"]
    const phoxName = infoDict["phox_name"]
    const phoxLevel = infoDict["phox_level"]
    const phoxStatus = infoDict["phox_status"]
    const phoxArt = infoDict["phox_art"]
    drawPhox(phoxMaxHP, phoxCurrentHP, phoxMaxRAM, phoxCurrentRAM, phoxName, phoxLevel, phoxStatus, phoxArt)
}

function drawWildPhox(maxhp, hp, maxram, ram, pname, lvl, status, art) {
    $("#enemyArt").html(art)
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

function drawPhox(maxhp, hp, maxram, ram, pname, lvl, status, art){
    $("#playerArt").html(art)
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
    // $.getJSON("https://api.ipify.org?format=json", function(data) {
    //     const ip = (data.ip)
    const sid = socket.id
    socket.emit('initialize encounter state', sid)
    // })
}

// Tells the client if its your turn, or tells you what the opponent did on its turn
function getTurnInfo() {
    const sid = socket.id
    socket.emit('get turn info', sid)
}

function drawPartyButton() {
    $('#content').append('<br><button id="viewParty">\
                            View Party\
                            </button>')
}

function drawParty(data) {
    $("#content").css("height", "135px")
    $("#content").css("width", "300px")
    $("#content").html("<div class='phox leader'>leader</div>")
    if (data[1]){
        $("#content").append("<div class='phox'>None</div>") 
    }
    if (data[2]){
        $("#content").append("<div class='phox'>None</div>")
    }
    drawPartyDetails(data)
}

function drawPartyDetails(data){
    for (i=0; i<3; i++) {
        if (data[i]){
            const phoxInfo = document.querySelectorAll("#content .phox")
            phox = data[i]
            phoxInfo[i].innerHTML = phox["species"]+"<br>\
                                    "+phox["nickname"]+"<br>\
                                    "+phox["stats"]["health"]+" /\
                                    "+phox["stats"]["max health"]+"HP"
        }
    }
}

function drawCollection(collection) {
    console.log(collection)
    $("#content").css("height", "300px")
    $("#content").append("<div id='collection'></div>")
    for (i=0; i<collection.length; i++){
        $("#collection").append("<div class='collectionPhox'>"+collection[i]+"</div>")
    }
}

function displayPhox(phoxSpecies){
    $("#content").css("height", "300px")
    $("#content").css("width", "300px")
    for (i=0; i<globalData.length; i++) {
        const phox = globalData[i]
        if (phox["species"] == phoxSpecies){
            displayPhoxDetails(phox)
        }
    }
}

function displayPhoxDetails(phox){
    globalPhox = phox
    viewPhoxAttacks(phox)
    viewPhoxBasicInfo(phox)
    viewPhoxStats(phox)
    viewPhoxUpgradesButton(phox)
}

function viewPhoxAttacks(phox) {
    globalAttacks = phox["attacks"]
    $("#content").html("<div id='attacks'></div>")
    for (i=0; i<phox.attacks.length; i++){
        $("#attacks").append("<div class='attack'>"+phox.attacks[i]["name"]+"</div>")
    }
}

function viewPhoxBasicInfo(phox) {
    $("#content").append("<div id='basicInfo'></div>")
    $("#basicInfo").append(phox["nickname"]+" the level "+phox["level"]+" ")
    $("#basicInfo").append(phox["species"]+"<br>")
    $("#basicInfo").append(phox["family"]+"<br>")
    $("#basicInfo").append(phox["stats"]["health"]+"/"+phox["stats"]["max health"]+" health")
}

function viewPhoxStats(phox) {
    $("#content").append("<div id='stats'></div>")
    $("#stats").append("CPOW: "+phox["stats"]["cpow"]+"<br>")
    $("#stats").append("LPOW: "+phox["stats"]["lpow"]+"<br>")
    $("#stats").append("CSEC: "+phox["stats"]["csec"]+"<br>")
    $("#stats").append("LSEC: "+phox["stats"]["lsec"]+"<br>")
    $("#stats").append("SPD: "+phox["stats"]["speed"]+"<br>")
    $("#stats").append("RR: "+phox["stats"]["rr"]+"<br>")
    $("#stats").append("VIS: "+phox["stats"]["vis"]+"<br>")
}

function viewPhoxUpgradesButton(phox) {
    $("#content").append("<div id='viewUpgrades'>Upgrades</div>")
}

function drawUpgradeMenu() {
    $("#content").append("<div id='baseUpgrades'></div>")
    $("#content").append("<div id='upgradeTree'></div>")
    const upgradeTree = globalPhox["upgrade tree"]
    const baseUpgrades = globalPhox["base upgrades"]
    drawBaseUpgrades(baseUpgrades)
    drawUpgradeTree(upgradeTree)
}

function drawBaseUpgrades(baseUpgrades){
    for (i=0; i<baseUpgrades.length; i++){
        const upgrade = baseUpgrades[i]
        $("#baseUpgrades").append("<div class='upgrade activated'>"+upgrade["name"]+"</div>")
    }
}

function drawUpgradeTree(upgradeTree) {
    $("#upgradeTree").html("")
    $("#upgradeTree").append("<div id='resetUpgrades'>Reset Upgrades</div>")
    for (i=0; i<upgradeTree.length; i++){
        $("#upgradeTree").append("<div class='upgradeTreeRow row"+i+"'>"+(i+1)+"</div>")
        for (n=0; n<upgradeTree[i].length; n++) {
            $(".row"+i).append("<div class='upgrade option"+n+"'>"+upgradeTree[i][n]["name"]+"</div>")
        }
    }
    checkForAcitavtedUpgrades()
}
function checkForAcitavtedUpgrades(){
    console.log(globalPhox["upgrade indexes"].length)
    for (i =0; i<globalPhox["upgrade indexes"].length; i++){
        const row = document.getElementsByClassName("row"+i)
        const adujusted_index = 1 + globalPhox["upgrade indexes"][i]
        const div = row[0].childNodes[adujusted_index]
        div.classList.add('activated')
    }
}