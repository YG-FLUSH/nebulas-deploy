#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   Author: Yoge
#   Time: 2018/06/04

from nebulas import Nebulas
from config import config
from optparse import OptionParser
import time
from huepy import red, green

def check_transaction(neb, txhash):
    result = neb.check_transaction(txhash)
    print result
    for i in range(40):
        result = neb.check_transaction(txhash)
        if result['status'] == 1:
            if 'contract_address' in result:
                print 'contract_address: %s' % result['contract_address']
            print green("Success!")
            break
        elif result['status'] == 0:
            print green("Fail!")
            break
        else:
            print green("."*i)
            print green("Peding!")
        time.sleep(7)


def main():
    parser = OptionParser()
    parser.add_option("-d", "--deploy", type="string", dest="contract_file", help=u"部署合约")
    parser.add_option("-c", "--call", type="string", dest="call", help=u"调用合约函数 'contract_address function arg1 arg2'")
    parser.add_option("-q", "--query", type="string", dest="query", help=u"查询合约数据 'contract_address function arg1 arg2'")
    parser.add_option("-t", "--txhash", type="string", dest="txhash", help=u"查看交易状态'")
    neb = Nebulas(config['domain'], config['address'], config['passphrase'])
    options, _ = parser.parse_args()

    contract_file = options.contract_file
    if contract_file:
        with open(contract_file) as f:
            contract = f.read()
        result = neb.deploy_contract(contract)
        print result
        check_transaction(neb, result['txhash'])

    call = options.call
    if call:
        _args = call.split(" ")
        if len(_args) < 2:
            print red("call function should have at lease two args")
            return
        _args.reverse()
        contract_address, function = _args.pop(), _args.pop()
        result = neb.call(contract_address, function, _args)
        print result
        check_transaction(neb, result['txhash'])

    query = options.query
    if query:
        _args = query.split(" ")
        if len(_args) < 2:
            print red("query function should have at lease two args")
            return
        _args.reverse()
        contract_address, function = _args.pop(), _args.pop()
        print neb.query(contract_address, function, _args)

    txhash = options.txhash
    if txhash:
        check_transaction(neb, txhash)



if __name__ == "__main__":
    main()

