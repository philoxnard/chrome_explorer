chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab){
    if (changeInfo.url){
        fetch('http://127.0.0.1:5000/test', {
            method: "post",
            mode: "no-cors",
            body: changeInfo.url,
            headers: new Headers({
                "content-type": "text/plain"
            })
        })
    }
})
