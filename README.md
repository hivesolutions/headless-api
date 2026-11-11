# [Headless API](http://headless-api.hive.pt)

[Headless](https://github.com/hivesolutions/headless) API Python client, to be used for simple synchronous integration.

## Configuration

| Name                  | Type  | Default                        | Description                                                                                          |
| --------------------- | ----- | ------------------------------ | ---------------------------------------------------------------------------------------------------- |
| **HEADLESS_BASE_URL** | `str` | `https://headless.bemisc.com/` | The base URL that is going to be used for API connections.                                           |
| **HEADLESS_KEY**      | `str` | `None`                         | The key sent in the `X-Headless-Key` header of the requests, required when Headless has one defined. |

## Example

```python
import headless

api = headless.API(key="my_key")
image = api.render("https://example.com/")
pdf = api.render_contents(
    "<html><head><style>@page { size: A3; }</style></head><body>Hello</body></html>",
    format="pdf",
    prefer_css_page_size=True,
)
with open("hello.pdf", "wb") as file:
    file.write(pdf)
print(api.info()["version"])
```

The parameters of `render()` (a URL) and `render_contents()` (an HTML document, sent as UTF-8) are the query parameters of Headless, described in its [README](https://github.com/hivesolutions/headless#parameters), with the boolean ones (eg: `prefer_css_page_size`) as `True` or `False`. The images and PDFs are returned as `bytes` and the errors of Headless (eg: `Invalid key`) are raised as `appier.HTTPError`. The key header and the HTML documents require Headless 0.3.0 or later.

## License

Headless API is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://github.com/hivesolutions/headless-api/workflows/Main%20Workflow/badge.svg)](https://github.com/hivesolutions/headless-api/actions)
[![PyPi Status](https://img.shields.io/pypi/v/headless-api.svg)](https://pypi.python.org/pypi/headless-api)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
