# HTTP Log

This document records five HTTP requests made using curl to a public JSON API. Each request includes the request sent, the response received, and an annotation of the status code and Content-Type.

## Request 1 — Get User 1

### Command

```powershell
curl.exe -v https://jsonplaceholder.typicode.com/users/1
```

### Request

```http
GET /users/1 HTTP/1.1
Host: jsonplaceholder.typicode.com
User-Agent: curl/8.21.0
Accept: */*
```

### Response

```http
HTTP/1.1 200 OK
Date: Sat, 15 Aug 2026 17:19:53 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 509
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"1fd-+2Y3G3w049iSZtw5t1mzSnunngE"
expires: -1
pragma: no-cache
Server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1786754590
Age: 2141
Accept-Ranges: bytes
cf-cache-status: HIT
CF-RAY: a2b9dde50cf5fb88-BOM
alt-svc: h3=":443"; ma=86400
```

### Response Body

```json
{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz",
  "address": {
    "street": "Kulas Light",
    "suite": "Apt. 556",
    "city": "Gwenborough",
    "zipcode": "92998-3874",
    "geo": {
      "lat": "-37.3159",
      "lng": "81.1496"
    }
  },
  "phone": "1-770-736-8031 x56442",
  "website": "hildegard.org",
  "company": {
    "name": "Romaguera-Crona",
    "catchPhrase": "Multi-layered client-server neural-net",
    "bs": "harness real-time e-markets"
  }
}
```

### Annotation

- **Status: 200 OK** — The server successfully processed the request and returned the requested user.
- **Content-Type: application/json** — The response body is JSON data.


## Request 2 — Get User 2

### Command

```powershell
curl.exe -v https://jsonplaceholder.typicode.com/users/2
```

### Request

```http
GET /users/2 HTTP/1.1
Host: jsonplaceholder.typicode.com
User-Agent: curl/8.21.0
Accept: */*
```

### Response

```http
HTTP/1.1 200 OK
Date: Sat, 15 Aug 2026 17:40:52 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 509
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"1fd-XTG63SYhaP/Uo6/vgmARnL3rpBk"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=Na8sQ0dGJO16UrwjH3bPMevqhFZ7w%2FCtVnj8yFsR%2Fmw%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786773780"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=Na8sQ0dGJO16UrwjH3bPMevqhFZ7w%2FCtVnj8yFsR%2Fmw%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786773780"
Server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 997
x-ratelimit-reset: 1786773823
Accept-Ranges: bytes
cf-cache-status: REVALIDATED
CF-RAY: a2b9fc9dbca68eeb-BOM
alt-svc: h3=":443"; ma=86400
```

### Response Body

```json
{
  "id": 2,
  "name": "Ervin Howell",
  "username": "Antonette",
  "email": "Shanna@melissa.tv",
  "address": {
    "street": "Victor Plains",
    "suite": "Suite 879",
    "city": "Wisokyburgh",
    "zipcode": "90566-7771",
    "geo": {
      "lat": "-43.9509",
      "lng": "-34.4618"
    }
  },
  "phone": "010-692-6593 x09125",
  "website": "anastasia.net",
  "company": {
    "name": "Deckow-Crist",
    "catchPhrase": "Proactive didactic contingency",
    "bs": "synergize scalable supply-chains"
  }
}
```

### Annotation

- **Status: 200 OK** — The server successfully processed the request and returned the requested user.
- **Content-Type: application/json** — The response body contains JSON data.


## Request 3 — Get Post 1

### Command

```powershell
curl.exe -v https://jsonplaceholder.typicode.com/posts/1
```

### Request

```http
GET /posts/1 HTTP/1.1
Host: jsonplaceholder.typicode.com
User-Agent: curl/8.21.0
Accept: */*
```

### Response

```http
HTTP/1.1 200 OK
Date: Sat, 15 Aug 2026 17:47:10 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 292
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"124-yiKdLzqO5gfBrJFrcdJ8Yq0LGnU"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=vm67FVLNHsCgrFgubRa04ooDeMKdgwXS9H3i2IbjuoY%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1785194657"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=vm67FVLNHsCgrFgubRa04ooDeMKdgwXS9H3i2IbjuoY%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1785194657"
Server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1785194663
Age: 6145
Accept-Ranges: bytes
cf-cache-status: HIT
CF-RAY: a2ba05dcfb923f78-BOM
alt-svc: h3=":443"; ma=86400
```

### Response Body

```json
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
```

### Annotation

- **Status: 200 OK** — The server successfully processed the request and returned the requested post.
- **Content-Type: application/json** — The response body contains JSON data.


## Request 4 — Get Non-Existent Post

### Command

```powershell
curl.exe -v https://jsonplaceholder.typicode.com/posts/9999
```

### Request

```http
GET /posts/9999 HTTP/1.1
Host: jsonplaceholder.typicode.com
User-Agent: curl/8.21.0
Accept: */*
```

### Response

```http
HTTP/1.1 404 Not Found
Date: Sat, 15 Aug 2026 17:50:05 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 2
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"2-vyGp6PvFo4RvsFtPoIWeCReyIC8"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=OTPv1x5hvtB%2BUkQvxLj%2BJbLo0HOiVaukzGFw1UT0Avk%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786790214"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=OTPv1x5hvtB%2BUkQvxLj%2BJbLo0HOiVaukzGFw1UT0Avk%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786790214"
Server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1786790263
Age: 25990
cf-cache-status: HIT
CF-RAY: a2ba0a2238223b0f-BOM
alt-svc: h3=":443"; ma=86400
```

### Response Body

```json
{}
```

### Annotation

- **Status: 404 Not Found** — The server received and processed the request, but the requested resource `/posts/9999` was not found.
- **Content-Type: application/json** — The response body contains JSON data. In this case, the body is an empty JSON object (`{}`).


## Request 5 — Create a User

### Command

```powershell
curl.exe -v -X POST -H "Content-Type: application/json" -d '{\"name\":\"Subh\"}' https://jsonplaceholder.typicode.com/users
```

### Request

```http
POST /users HTTP/1.1
Host: jsonplaceholder.typicode.com
User-Agent: curl/8.21.0
Accept: */*
Content-Type: application/json
Content-Length: 15
```

### Request Body

```json
{
  "name": "Subh"
}
```

### Response

```http
HTTP/1.1 201 Created
Date: Sat, 15 Aug 2026 17:54:33 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 32
Connection: keep-alive
access-control-allow-credentials: true
access-control-expose-headers: Location
Cache-Control: no-cache
etag: W/"20-6zp2j680IHOGBXLBCUjiB/O2Gbk"
expires: -1
location: https://jsonplaceholder.typicode.com/users/11
nel: {"report_to":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=ysIpn%2BlpN18WAaByG%2BBvbRFivzJezfAXDswt1XqG5gI%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786816472"}],"max_age":3600}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=ysIpn%2BlpN18WAaByG%2BBvbRFivzJezfAXDswt1XqG5gI%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786816472"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=ysIpn%2BlpN18WAaByG%2BBvbRFivzJezfAXDswt1XqG5gI%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786816472"
Server: cloudflare
vary: Origin, X-HTTP-Method-Override, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1786816483
cf-cache-status: DYNAMIC
CF-RAY: a2ba10a91aef4419-BOM
alt-svc: h3=":443"; ma=86400
```

### Response Body

```json
{
  "name": "Subh",
  "id": 11
}
```

### Annotation

- **Status: 201 Created** — The server successfully processed the POST request and created a new user resource.
- **Content-Type: application/json** — The response body contains JSON data.
- **Location** — The header identifies the URL of the newly created user resource: `https://jsonplaceholder.typicode.com/users/11`.