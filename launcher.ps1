
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

param ($run,$port)

write-host $args
write-host $run,$port