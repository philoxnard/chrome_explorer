const form = document.getElementById('getPlayer')

if (form) {
    form.addEventListener('submit', function(){
        const req = new XMLHttpRequest()
        const baseUrl = "http://127.0.0.1:5000"
        const username = document.getElementById("username").value
        $.post(baseUrl+"/login", {
            username: username
        })
        $.post(baseUrl+"/test", {
            data: "does this work"
        })
    })
}
