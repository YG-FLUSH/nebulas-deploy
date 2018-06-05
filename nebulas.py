#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   Author: Yoge
#   Time: 2018/06/04

import json
import urlparse
import requests

class Nebulas(object):

    def __init__(self, domain, address, passphrase):
        self.domain = domain
        self.address = address
        self.passphrase = passphrase

    def send_request(self, url, data, headers=None):
        if not headers:
            headers = {
                "Accept": "application/json",
            }
        # Let the network errors go
        data = json.dumps(data)
        result = requests.post(url, data=data, headers=headers)
        result = result.json()
        if 'result' in result:
            return result['result']
        else:
            raise Exception(str(result))

    def admin_sign(self, data):
        url = urlparse.urljoin(self.domain, "/v1/admin/sign")
        result = self.send_request(url, data)
        data = result['data']
        return data

    def raw_transaction(self, data):
        url = urlparse.urljoin(self.domain, "/v1/user/rawtransaction")
        data = {
            'data': data
        }
        result = self.send_request(url, data)
        return result

    def transaction(self, to, value):
        return self._transaction(to, value)

    def _transaction(self, to, value, contract=None):
        # 签名 & 发送 的方式
        state = self.get_account_state()
        nonce = int(state['nonce']) + 1
        data = {
            "transaction":{
                "from": self.address,
                "to": to,
                "value": str(value),
                "nonce": str(nonce),
                "gasPrice": "1000000",
                "gasLimit": "2000000",
            },
            "passphrase": self.passphrase
        }
        if contract:
            data['transaction']['contract'] = contract
        data = self.admin_sign(data)
        # {"result":{"txhash":"1b8cc3f977256c4d620b7d72f531bc19f10eb13a05ff24a8a792cd5da53a1277","contract_address":""}}
        return self.raw_transaction(data)

    def deploy_contract(self, contract, source_type="js", args=""):
        # 签名 & 发送 的方式
        source = contract
        contract_dict = {
            'source': source,
            "sourceType": source_type,
            "args": args,
        }
        return self._transaction(self.address, 0, contract_dict)

    def call(self, contract_address, function, args, value=0):
        to = contract_address
        contract_dict = {
            'function': function,
            'args': "[%s]" % (",".join(args)),
        }
        return self._transaction(to, value, contract_dict)

    def query(self, contract_address, function, args):
        state = self.get_account_state()
        nonce = int(state['nonce']) + 1
        data = {
            "from": self.address,
            "to": contract_address,
            "value": "0",
            "nonce": str(nonce),
            "gasPrice": "1000000",
            "gasLimit": "2000000",
            "contract": {
                "function": function,
                'args': "[%s]" % (",".join(args)),
            }
        }
        url = urlparse.urljoin(self.domain, "/v1/user/call")
        return self.send_request(url, data)

    def get_account_state(self):
        url = urlparse.urljoin(self.domain, "/v1/user/accountstate")
        data = {'address': self.address}
        #{"result":{"balance":"0","nonce":"0","type":87}}
        return self.send_request(url, data)

    def check_transaction(self, txhash):
        url = urlparse.urljoin(self.domain, "/v1/user/getTransactionReceipt")
        data = {'hash': txhash}
        return self.send_request(url, data)



