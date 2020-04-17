#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import hashlib
import argparse


def sign_parameters(params, secret):
    # params need to be sorted by key
    ordered_params = sorted(params.items())
    tmp_data = []

    for key, value in ordered_params:
        tmp_data.append("{0}:{1}".format(key, value))

    request_data_string = "|".join(tmp_data)
    request_data_string += secret

    params["hash"] = hashlib.md5(request_data_string.encode("utf-8")).hexdigest()
    return params


def make_request(url, data, app_secret):
    try:
        data = json.loads(data)
    except Exception as ex:
        print("Post Data inválido: {}".format(ex))
        exit(0)

    data = sign_parameters(data, app_secret)
    data = urllib.urlencode(data).encode()

    req = urllib2.Request(url, data=data)

    response = urllib2.urlopen(req)
    print(response.read())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Wobiz Request')
    parser.add_argument('-u', '--url', required=True, help='Wobiz API URL')
    parser.add_argument('-s', '--secret', required=True, help='Wobiz Secret Key')
    parser.add_argument('-d', '--data', required=True, help='''Post Data, 
        ex.: { "user_id": "812371", "type": "one_shot", "start_at": "2020-01-21 11:00:00", "end_at": "2020-02-21 11:00:00", "api_key": "api_key" }''')
    perse_args = parser.parse_args()

    make_request(perse_args.url, perse_args.data, perse_args.secret)
