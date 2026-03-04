
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

enum {
    server,
    scraper,
    scraperTestClient
}

param (
    [string]server,
    [string]scraper,
    [string]scraperTestClient,
)