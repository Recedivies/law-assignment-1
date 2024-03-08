#!/bin/bash

# Set the request body as a variable
request_body='{
    "method": "GET",
    "host": "my.photos",
    "path": "/photos",
    "service_id": "cf55763e-a4c0-4b1b-bbc7-b847cc65dd75"
}'

# Send the POST request using `hey`
hey -m POST \
-n 100 -c 50 \
-H "Authorization: Token 8c554b86ac796a2a641fed3b9640a60a42a0ef7b" \
-H "Content-Type: application/json" \
-d "$request_body" \
http://localhost:8000/requests/
