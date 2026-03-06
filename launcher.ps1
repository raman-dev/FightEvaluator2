
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
    [int]$port,
    [string]$withScraper,
    [string]$launchBrowser="false"
)

$launchBrowser = $launchBrowser.ToLower()

switch ($service){
    "web-server" {
        write-host "Starting Web-Server"
        if ($launchBrowser -eq "true"){
            write-host "Launching Chrome"
            start chrome "http://localhost:8080"
        }
        pipenv run pwsh "run-server.ps1"
    }
    "scraper" {
        write-host "Starting Scraper"
        # this is batch file so i can rename new process window
        pipenv run "run-scraper.bat" 
    }
    "scraper-test-client"{
        write-host "starting scraper-test-client"
    }
}