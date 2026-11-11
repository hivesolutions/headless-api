#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Headless API
# Copyright (c) 2008-2026 Hive Solutions Lda.
#
# This file is part of Hive Headless API.
#
# Hive Headless API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Headless API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Headless API. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2026 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """


import unittest

import appier

import headless


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.api = headless.API(base_url="https://headless.hive.pt/")
        self.api.get = lambda url, **kwargs: self._request("GET", url, **kwargs)
        self.api.post = lambda url, **kwargs: self._request("POST", url, **kwargs)
        self.requests = []

    def _request(self, method, url, **kwargs):
        self.requests.append((method, url, kwargs))
        return b"%PDF-1.4"

    def test_basic(self):
        self.assertEqual(1 + 1, 2)

    def test_base_url(self):
        api = headless.API()
        api.get = lambda url, **kwargs: url
        self.assertEqual(api.base_url, "https://headless.bemisc.com/")
        self.assertEqual(api.key, None)
        self.assertEqual(api.info(), "https://headless.bemisc.com/info")

    def test_key(self):
        api = headless.API(base_url="https://headless.hive.pt/", key="secret")
        self.assertEqual(api.base_url, "https://headless.hive.pt/")
        self.assertEqual(api.key, "secret")

    def test_build(self):
        headers = dict(Accept="application/pdf")
        self.api.build("GET", self.api.base_url, headers=headers, kwargs=dict())
        self.assertEqual(headers, dict(Accept="application/pdf"))

        # the key is sent in the header (and never in the query) of
        # every request, as Headless accepts it in both
        api = headless.API(key="secret")
        headers = dict(Accept="application/pdf")
        params = dict(url="https://example.com/")
        api.build("GET", api.base_url, headers=headers, params=params, kwargs=dict())
        self.assertEqual(
            headers, {"Accept": "application/pdf", "X-Headless-Key": "secret"}
        )
        self.assertEqual(params, dict(url="https://example.com/"))

    def test_render(self):
        result = self.api.render("https://example.com/", format="pdf")
        self.assertEqual(result, b"%PDF-1.4")
        method, url, kwargs = self.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "https://headless.hive.pt/")
        self.assertEqual(kwargs["params"]["url"], "https://example.com/")
        self.assertEqual(kwargs["params"]["format"], "pdf")
        self.assertEqual(
            sorted(key for key, value in kwargs["params"].items() if not value == None),
            ["format", "url"],
        )

        # the boolean parameters are sent as the flags read by Headless
        # (1 or 0), and left out when no value is provided
        self.api.render(
            "https://example.com/",
            prefer_css_page_size=True,
            print_background=False,
            full_page=False,
            trim=True,
            reload=False,
        )
        _method, _url, kwargs = self.requests[1]
        self.assertEqual(kwargs["params"]["prefer_css_page_size"], "1")
        self.assertEqual(kwargs["params"]["print_background"], "0")
        self.assertEqual(kwargs["params"]["full_page"], "0")
        self.assertEqual(kwargs["params"]["trim"], "1")
        self.assertEqual(kwargs["params"]["reload"], "0")

        self.api.render(
            "https://example.com/",
            width=400,
            height=300,
            scale_factor=2,
            timeout=500,
            cookie=["session,secret", "lang,pt"],
            method="POST",
            engine="phantom",
        )
        _method, _url, kwargs = self.requests[2]
        self.assertEqual(kwargs["params"]["width"], 400)
        self.assertEqual(kwargs["params"]["height"], 300)
        self.assertEqual(kwargs["params"]["scale_factor"], 2)
        self.assertEqual(kwargs["params"]["timeout"], 500)
        self.assertEqual(kwargs["params"]["cookie"], ["session,secret", "lang,pt"])
        self.assertEqual(kwargs["params"]["method"], "POST")
        self.assertEqual(kwargs["params"]["engine"], "phantom")
        self.assertEqual(kwargs["params"]["print_background"], None)

    def test_render_contents(self):
        result = self.api.render_contents(
            "<html></html>", format="pdf", prefer_css_page_size=True
        )
        self.assertEqual(result, b"%PDF-1.4")
        method, url, kwargs = self.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "https://headless.hive.pt/")
        self.assertEqual(kwargs["data"], b"<html></html>")
        self.assertEqual(kwargs["mime"], "text/html")
        self.assertEqual(kwargs["params"]["format"], "pdf")
        self.assertEqual(kwargs["params"]["prefer_css_page_size"], "1")
        self.assertEqual(
            sorted(key for key, value in kwargs["params"].items() if not value == None),
            ["format", "prefer_css_page_size"],
        )
        self.assertEqual("url" in kwargs["params"], False)

        # the unicode contents are sent as UTF-8 (the encoding read by
        # Headless), even with characters outside Latin-1 (eg: the euro)
        self.api.render_contents(appier.legacy.u("<p>Peça €</p>"))
        _method, _url, kwargs = self.requests[1]
        self.assertEqual(
            kwargs["data"], appier.legacy.u("<p>Peça €</p>").encode("utf-8")
        )

        self.api.render_contents(b"<p>Pe\xc3\xa7a</p>", mime="application/xhtml+xml")
        _method, _url, kwargs = self.requests[2]
        self.assertEqual(kwargs["data"], b"<p>Pe\xc3\xa7a</p>")
        self.assertEqual(kwargs["mime"], "application/xhtml+xml")

        self.api.render_contents(
            "<html></html>",
            print_background=False,
            full_page=True,
            trim=False,
            reload=True,
            wait_until="networkidle0",
            page_format="A3",
            width=400,
            height=300,
            scale_factor=2,
            timeout=500,
        )
        _method, _url, kwargs = self.requests[3]
        self.assertEqual(kwargs["params"]["print_background"], "0")
        self.assertEqual(kwargs["params"]["full_page"], "1")
        self.assertEqual(kwargs["params"]["trim"], "0")
        self.assertEqual(kwargs["params"]["reload"], "1")
        self.assertEqual(kwargs["params"]["wait_until"], "networkidle0")
        self.assertEqual(kwargs["params"]["page_format"], "A3")
        self.assertEqual(kwargs["params"]["width"], 400)
        self.assertEqual(kwargs["params"]["height"], 300)
        self.assertEqual(kwargs["params"]["scale_factor"], 2)
        self.assertEqual(kwargs["params"]["timeout"], 500)

    def test_info(self):
        result = self.api.info()
        self.assertEqual(result, b"%PDF-1.4")
        self.assertEqual(self.requests, [("GET", "https://headless.hive.pt/info", {})])

        # the route is appended to the base URL with a single slash, whether
        # or not the base URL ends with one, keeping its path (if any)
        for base_url, url in (
            ("http://localhost:3000", "http://localhost:3000/info"),
            ("http://localhost:3000/", "http://localhost:3000/info"),
            ("https://hive.pt/headless", "https://hive.pt/headless/info"),
            ("https://hive.pt/headless/", "https://hive.pt/headless/info"),
        ):
            api = headless.API(base_url=base_url)
            api.get = lambda url, **kwargs: url
            self.assertEqual(api.info(), url)
