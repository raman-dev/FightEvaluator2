
# how to do this?
# requirements
# ----------------
#     launch my services with my options 

#     services
#     --------
#     scraper 
#     web-server
#     scraper-test-client

#     server launch options
#         no  options
#         port option -> --port [int]
#     scraper launch options
#         no options
#     scraper-test-client 
#         no options

<#
    script.ps1 -param0 value arg0 arg1 -param1 value
    powershell filters args into positional args array
    and key words with values into parameters

    if switch is arguements will be used as positional parameters
#>

param (
    [string]$service,
    [int]$port=8080,
    [switch]$withScraper,
    [switch]$launchBrowser
)

function RunWebServer {
    param (
        [int]$port,
        [switch]$startWithBrowser,
        [switch]$startWithScraper
    )
    write-host "Starting Web-Server"
    if ($startWithBrowser){
        write-host "Launching Chrome"
        start chrome "http://localhost:$port"
    }
    if ($startWithScraper){
        RunScaper
    }
    pipenv run pwsh "run-server.ps1"
}

function RunScaper{
    write-host "Starting Scraper"
    # this is batch file so i can rename new process window
    pipenv run "run-scraper.bat" 
}

switch ($service){
    "web-server" {
        RunWebServer -port $port -startWithBrowser:$launchBrowser -startWithScraper:$withScraper
    }
    "scraper" {
        RunScaper
    }
    "scraper-test-client"{
        write-host "starting scraper-test-client"
    }
    default {
        write-host "options [web-server,scraper,scraper-test-client]"
    }
}