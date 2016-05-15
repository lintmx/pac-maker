function FindProxyForURL(url, host) {
    var direct = 'DIRECT';
    var proxy = '__PROXY_ADDRESS__';
    
    var specialList = __SPECIALLIST__;
    var whiteList = __WHITELIST__;
    var blackList = __BLACKLIST__;
    var chinaIP = __CHINAIP__;
    
    function toInt(ipString) {
        var ipArray = ipString.split('.');
        return ipArray[0] * 65536 + ipArray[1] * 256 + ipArray[2] * 1;
    }
    
    function binarySearch(ip, list) {
        var left = 0;
        var right = list.length - 1;
        
        do {
            var mid = Math.floor((left + right) / 2);
            
            if (Math.abs(ip - list[mid][0]) <= list[mid][1]) {
                return true;
            } else if (ip > list[mid][0]) {
                left = mid;
            } else {
                right = mid;
            }
        } while (left < right - 1);
        
        return false;
    }
    
    if (isPlainHostName(host)) {
        return direct;
    }
    
    if (specialList.hasOwnProperty(host)) {
        if (specialList[host] == 1) {
            return direct;
        } else {
            return proxy;
        }
    }
   
    var hostArray = host.split('.');
    var currHost = hostArray[hostArray.length - 1];

    for (var i = hostArray.length - 2;i > -1;i--) {
        if (whiteList.hasOwnProperty(currHost)) {
            return direct;
        }
        if (blackList.hasOwnProperty(currHost)) {
            return proxy;
        }
        currHost = hostArray[i] + '.' + currHost;
    } 
    
    var ipString = toInt(dnsResolve(host));
    
    if (binarySearch(ipString, chinaIP)) {
        return direct;
    }
    
    return proxy;
}
