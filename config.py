config = {
    'intelUrls' : [
        'http://mirror1.malwaredomains.com/files/justdomains',
        ],
    'bindZoneFilePath' : '/etc/bind',
    'blocklistName':"blocklist.block",
    'blocklistTTL':180,
    'blocklistRefresh':1200,
    'blocklistRetry':180,
    'blocklistExpiry':1209600,
    'blocklistNxDomainTTL':180,
    'blocklistA':'127.0.0.1',
    'blocklistDnsServers' : [
        "192.168.0.114",
        "192.168.0.117",
        ],
    'rpzListName':"rpz.zone",
    'rpzCnameTo':"blocked.block.",
    'rpzTTL':180,
    'rpzRefresh':1200,
    'rpzRetry':180,
    'rpzExpiry':1209600,
    'rpzNxDomainTTL':180,
}
