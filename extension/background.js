chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab){
    if (changeInfo.url){
        fetch('http://127.0.0.1:5000/test', {
            method: "post",
            body: changeInfo.url,
            headers: new Headers({
                "content-type": "text/plain"
            })
        })
        .then(function(response) {
            response.json().then(function(data) {
                console.log(data)
                if (data.state == "initialize encounter"){
                    console.log("You did it")
                    chrome.notifications.create('', {
                        title: "You found a phox",
                        message: "Look at that pretty phox",
                        iconUrl: "https://i.pinimg.com/564x/f0/c4/04/f0c404c8486dea5ab74ff001af848ab7.jpg",
                        type: 'basic'
                    })
                }
            })
        })
    }
})
