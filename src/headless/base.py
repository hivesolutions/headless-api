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

import appier

BASE_URL = "https://headless.bemisc.com/"
""" The default base URL to be used when no other
base URL value is provided to the constructor """


class API(appier.API):
    """
    Implementation of the Headless API specification
    for a simplified python client usage.
    """

    def __init__(self, *args, **kwargs):
        appier.API.__init__(self, *args, **kwargs)
        self.base_url = appier.conf("HEADLESS_BASE_URL", BASE_URL)
        self.key = appier.conf("HEADLESS_KEY", None)
        self.base_url = kwargs.get("base_url", self.base_url)
        self.key = kwargs.get("key", self.key)

    def build(
        self,
        method,
        url,
        data=None,
        data_j=None,
        data_m=None,
        headers=None,
        params=None,
        mime=None,
        kwargs=None,
    ):
        if self.key:
            headers["X-Headless-Key"] = self.key

    def render(
        self,
        url,
        format=None,
        page_format=None,
        prefer_css_page_size=None,
        print_background=None,
        wait_until=None,
        full_page=None,
        trim=None,
        width=None,
        height=None,
        scale_factor=None,
        timeout=None,
        cookie=None,
        method=None,
        reload=None,
        engine=None,
    ):
        contents = self.get(
            self.base_url,
            params=dict(
                url=url,
                format=format,
                page_format=page_format,
                prefer_css_page_size=_flag(prefer_css_page_size),
                print_background=_flag(print_background),
                wait_until=wait_until,
                full_page=_flag(full_page),
                trim=_flag(trim),
                width=width,
                height=height,
                scale_factor=scale_factor,
                timeout=timeout,
                cookie=cookie,
                method=method,
                reload=_flag(reload),
                engine=engine,
            ),
        )
        return contents

    def render_contents(
        self,
        contents,
        mime="text/html",
        format=None,
        page_format=None,
        prefer_css_page_size=None,
        print_background=None,
        wait_until=None,
        full_page=None,
        trim=None,
        width=None,
        height=None,
        scale_factor=None,
        timeout=None,
        reload=None,
    ):
        # encodes the (unicode) contents as UTF-8, the encoding expected
        # by Headless, as they would otherwise be sent as Latin-1
        contents = appier.legacy.bytes(contents, encoding="utf-8", force=True)
        contents = self.post(
            self.base_url,
            data=contents,
            mime=mime,
            params=dict(
                format=format,
                page_format=page_format,
                prefer_css_page_size=_flag(prefer_css_page_size),
                print_background=_flag(print_background),
                wait_until=wait_until,
                full_page=_flag(full_page),
                trim=_flag(trim),
                width=width,
                height=height,
                scale_factor=scale_factor,
                timeout=timeout,
                reload=_flag(reload),
            ),
        )
        return contents

    def info(self):
        url = self.base_url + "info"
        contents = self.get(url)
        return contents


def _flag(value):
    """
    Converts the provided (boolean) value into the flag value
    expected by Headless for its boolean parameters, so that the
    parameter is not sent when the value is not provided.

    :type value: bool
    :param value: The value to be converted, None for the default
    value of Headless.
    :rtype: String
    :return: The flag value of the parameter, 1 or 0, or None when
    no value is provided.
    """

    if value == None:
        return None
    return "1" if value else "0"


class Info(dict):
    pass
