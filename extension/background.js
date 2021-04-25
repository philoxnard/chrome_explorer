chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab){
    if (changeInfo.url){
        fetch('http://127.0.0.1:5000/newUrl', {
            method: "post",
            body: changeInfo.url,
            headers: new Headers({
                "content-type": "text/plain"
            })
        })
        .then(function(response) {
            response.json().then(function(data) {
                console.log(data)
                // Manifest V3 apparently doesnt work for notifications, so
                // this will eventually get implemented as written
                // Currently works as a desktop notification, which is fine
                // But I'm going to copy/paste here the chrome notification syntax
                ////////////////////////////////////////////////////////////
                // if (data.state == "initialize encounter"){
                //     console.log("You did it")
                //     chrome.notifications.create('', {
                //         title: "You found a phox",
                //         message: "Look at that pretty phox",
                //         iconUrl: "notification.png",
                //         type: 'basic'
                //     })
                // }
                /////////////////////////////////////////////////////////////
                if (data.state == "initialize encounter"){
                    console.log("You did it")
                    registration.showNotification('Phoxtrot', {
                        body: "You found a phox! Click the extention to fight it!",
                    })
                }
            })
        })
    }
})


chrome.tabs.onRemoved.addListener(function(tabid, removed){
    fetch('http://127.0.0.1:5000/exit')
    .then(function() {
        console.log('Closing response detected')
    })
})

addEventListener('unload', function(){
    fetch('http://127.0.0.1:5000/exit')
    .then(function() {
        console.log('Closing response detected')
    })
})

addEventListener('beforeunload', function(){
    fetch('http://127.0.0.1:5000/exit')
    .then(function() {
        console.log('Closing response detected')
    })
})