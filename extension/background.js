const addr = 'http://127.0.0.1:5000'
// "http:18.222.237.192:8000"

chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab){
    if (changeInfo.url){
        fetch(addr+'/newUrl', {
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

                    // Experimenting with what's the best way to alert the user that they found a phox.
                    // The notification thing is probably best, but iirc it didn't work when the program
                    // was hosted on AWS and I'm not sure why.

                    // registration.showNotification('Phoxtrot', {
                    //     body: "You found a phox! Click the extention to fight it!",
                    // })
                    alert("You found a Phox! Click the extention to fight it!")
                }
            })
        })
    }
})


// chrome.tabs.onRemoved.addListener(function(tabid, removed){
//     fetch(addr+'/exit')
//     .then(function() {
//         console.log('Closing response detected')
//     })
// })

// addEventListener('unload', function(){
//     fetch(addr+'/exit')
//     .then(function() {
//         console.log('Closing response detected')
//     })
// })

// addEventListener('beforeunload', function(){
//     fetch(addr+'/exit')
//     .then(function() {
//         console.log('Closing response detected')
//     })
// })