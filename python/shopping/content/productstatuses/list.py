#!/usr/bin/python
#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Gets the status of all products on the specified account."""

from __future__ import print_function

import argparse
import json
import sys

from shopping.content import common

# The maximum number of results to be returned in a page.
MAX_PAGE_SIZE = 50

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument(
    "account_id",
    nargs="?",
    default=0,
    type=int,
    help="The ID of the account for which to get information.",
)


def main(argv):
    service, config, flags = common.init(argv, __doc__, parents=[argparser])
    account_id = flags.account_id

    if not account_id:
        account_id = config["merchantId"]
        print("No account ID provided. Use account ID in config instead.")

    request = service.productstatuses().list(
        merchantId=account_id, maxResults=MAX_PAGE_SIZE
    )

    print("This is the product status of account {}".format(account_id))

    while request is not None:
        result = request.execute()
        statuses = result.get("resources")
        if not statuses:
            print("No product statuses were returned.")
            break
        for stat in statuses:
            print(
                '- Product "%s" with title "%s":' % (stat["productId"], stat["title"])
            )
            print(json.dumps(stat, sort_keys=True, indent=2, separators=(",", ": ")))
        request = service.productstatuses().list_next(request, result)


if __name__ == "__main__":
    main(sys.argv)
