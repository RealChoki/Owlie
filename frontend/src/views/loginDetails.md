spotify:
1. their own page to specify from what uni ur
2. then a page Verify using your school credentials:
    https://services.sheerid.com/verify/63fd266996552d469aea40e1/?country=DE&locale=de&verificationId=676bea523ece042062000125#_gl=1*i4w63k*_gcl_au*MTAzMDA5NTYxOC4xNzM1MTI1NTg5
3. 2nd page leads u to htw login: 
    https://weblogin.htw-berlin.de/idp/profile/SAML2/Redirect/SSO?execution=e1s2

    after logged in:
    https://weblogin.htw-berlin.de/idp/profile/SAML2/Redirect/SSO?execution=e1s3

    You are about to access the service:
    SheerID Verification Services of SheerId

    Description as provided by this service:
    Student and Teacher Eligibility Verification Services for Global Brands




HTW schemas:
https://schema.htw-berlin.de



mmight be something:
define("format_tiles/registration", ["jquery", "core/notification", "core/config", "core/str"], (function($, Notification, config, str) {
    return {
        attemptRegistration: function(sesskey, serverUrl, data) {
            data.useragent = navigator.userAgent,
            data.browserlanguages = navigator.languages,
            $(document).ready((function() {
                $.ajax({
                    url: serverUrl,
                    type: "POST",
                    crossDomain: !0,
                    contentType: "application/json",
                    data: JSON.stringify(data),
                    dataType: "json",
                    success: function(data) {
                        if (data.status) {
                            str.get_strings([{
                                key: "registration",
                                component: "admin"
                            }, {
                                key: "registeredthanks",
                                component: "format_tiles"
                            }, {
                                key: "registerclicktocomplete",
                                component: "format_tiles"
                            }, {
                                key: "ok",
                                component: "format_tiles"
                            }, {
                                key: "cancel",
                                component: "moodle"
                            }]).done((function(s) {
                                Notification.confirm(s[0], s[1] + " " + s[2], s[3], s[4], (function() {
                                    window.location.href = config.wwwroot + "/course/format/tiles/editor/register.php?key=" + data.key + "&sesskey=" + sesskey
                                }), (function() {
                                    window.location.href = config.wwwroot + "/admin/settings.php?section=formatsettingtiles"
                                }))
                            }))
                        }
                    },
                    error: function(e) {
                        require(["core/log"], (function(log) {
                            log.debug("Error registering", e.message)
                        }))
                    }
                })
            }))
        }
    }
}));




Summary
URL: https://moodle.htw-berlin.de/login/index.php
URL: https://moodle.htw-berlin.de/login/index.php?testsession=75364
URL: https://moodle.htw-berlin.de/my/
Status: 200 OK
Source: Network
Address: 141.45.192.45:443

Request
POST /login/index.php
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Content-Type: application/x-www-form-urlencoded
Origin: https://moodle.htw-berlin.de
Referer: https://moodle.htw-berlin.de/login/index.php
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15

Redirect Response
303 See Other
Cache-Control: no-store
Date: Wed, 25 Dec 2024 12:47:40 GMT
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Location: https://moodle.htw-berlin.de/login/index.php?testsession=75364
Pragma: no-cache

Request
GET /login/index.php
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: en-GB,en;q=0.9
Referer: https://moodle.htw-berlin.de/login/index.php
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15

Redirect Response
303 See Other
Cache-Control: no-store
Date: Wed, 25 Dec 2024 12:47:40 GMT
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Location: https://moodle.htw-berlin.de/my/
Pragma: no-cache

Request
GET /my/ HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: en-GB,en;q=0.9
Connection: keep-alive
Cookie: MoodleSession=datvlnuuiq85nsocu6cc9tm7ur
Host: moodle.htw-berlin.de
Referer: https://moodle.htw-berlin.de/login/index.php
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15

Response
HTTP/1.1 200 OK
Accept-Ranges: none
Cache-Control: private, pre-check=0, post-check=0, max-age=0, no-transform
Connection: Keep-Alive
Content-Encoding: gzip
Content-Language: de
Content-Length: 23035
Content-Script-Type: text/javascript
Content-Style-Type: text/css
Content-Type: text/html; charset=utf-8
Date: Wed, 25 Dec 2024 12:47:40 GMT
Expires
Keep-Alive: timeout=5, max=98
Pragma: no-cache
Server: Apache
Strict-Transport-Security: max-age=63072000; includeSubdomains; preload
Vary: Accept-Encoding
X-Frame-Options: sameorigin
X-UA-Compatible: IE=edge

Request Data
MIME Type
Request Data: 
## this gives u moodle data?
anchor=&logintoken=GzKBbNZ6nsUNfO5jCkId8HEl7quFeeT8&username=s0589543&password=123123



# google chrome inspection network:
    log in post:
    Request URL:
https://moodle.htw-berlin.de/login/index.php
Request Method:
POST
Status Code:
303 See Other
Remote Address:
141.45.192.45:443
Referrer Policy:
strict-origin-when-cross-origin
cache-control:
no-store
connection:
Keep-Alive
content-language:
de
content-length:
1553
content-type:
text/html; charset=utf-8
date:
Wed, 25 Dec 2024 14:32:14 GMT
expires:
Thu, 19 Nov 1981 08:52:00 GMT
keep-alive:
timeout=5, max=100
location:
https://moodle.htw-berlin.de/login/index.php?testsession=75364
pragma:
no-cache
server:
Apache
set-cookie:
MoodleSession=mrn0srenn5r6jj2amt4re5grff; path=/; secure; SameSite=None
set-cookie:
MOODLEID1_=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT; Max-Age=0; path=/; secure
strict-transport-security:
max-age=63072000; includeSubdomains; preload
x-redirect-by:
Moodle
accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
accept-encoding:
gzip, deflate, br, zstd
accept-language:
en-GB,en-US;q=0.9,en;q=0.8
cache-control:
no-cache
connection:
keep-alive
content-length:
91
content-type:
application/x-www-form-urlencoded
cookie:
MoodleSession=ctq7a0gn4udsaepghv91iqgh8n
host:
moodle.htw-berlin.de
origin:
https://moodle.htw-berlin.de
pragma:
no-cache
referer:
https://moodle.htw-berlin.de/login/index.php
sec-ch-ua:
"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"
sec-ch-ua-mobile:
?0
sec-ch-ua-platform:
"macOS"
sec-fetch-dest:
document
sec-fetch-mode:
navigate
sec-fetch-site:
same-origin
sec-fetch-user:
?1
upgrade-insecure-requests:
1
user-agent:
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36


then it gets this:
https://moodle.htw-berlin.de/login/index.php?testsession=75364

so then it rederects (get) to /my