# Network Analysis

This document analyzes the network activity of the JSONPlaceholder website using the browser Developer Tools Network panel. The browser cache was disabled before reloading the page.

## Page Analyzed

```text
https://jsonplaceholder.typicode.com/
```

## Network Summary

### Request Count

```text
20 requests
```

A total of 20 HTTP requests were observed while loading the page.

### Total Page Size

```text
1.0 MB resources
```

The Network panel shows that the total size of the resources loaded by the page was approximately 1.0 MB.

The panel also shows:

```text
651 kB transferred
```

This represents the amount of data transferred over the network.

### Slowest Resource

The slowest resource observed was:

```text
553780578-52b3039d-1e4c-4c68-951c-93f0f1e73611.png...nedH...
```

Its size was approximately:

```text
341 kB
```

and it took:

```text
1.79 s
```

to load.

Therefore, this PNG image was the single slowest resource in the captured page load.

## 3xx and 4xx Responses

Two resources returned a `302` status code:

```text
adfee31f-a8b6-4684-9ab9-af4f03ac5b75 → 302
52b3039d-1e4c-4c68-951c-93f0f1e73611 → 302
```

### Meaning of 302

`302 Found` indicates a temporary redirect. The browser is instructed to request the resource from another location.

No `4xx` responses were observed in the captured Network log.

## Observation

The page generated 20 requests during loading. Most resources returned successful `200` responses. Two resources returned `302` redirects, while no client-error responses (`4xx`) were observed.

The largest and slowest resource visible in the captured Network log was a PNG image, which took 1.79 seconds to load and accounted for approximately 341 kB of resource size.