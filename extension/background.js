chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab){
    if (changeInfo.url){
        chrome.runtime.sendMessage({
            msg: changeInfo.url
        })
    }
})