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

from . import base


class HeadlessApp(appier.WebApp):

    def __init__(self, *args, **kwargs):
        appier.WebApp.__init__(self, name="headless", *args, **kwargs)

    @appier.route("/", "GET")
    def index(self):
        return self.info()

    @appier.route("/info", "GET")
    def info(self):
        api = self.get_api()
        result = api.info()
        return result

    @appier.route("/render", "GET")
    def render(self):
        url = self.field("url", mandatory=True)
        api = self.get_api()
        result = api.render(url, format="png")
        self.content_type("image/png")
        return result

    def get_api(self):
        return base.get_api()


if __name__ == "__main__":
    app = HeadlessApp()
    app.serve()
else:
    __path__ = []
