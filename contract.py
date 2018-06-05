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
    parser.add_option("-c", "--call", type="string", dest="call", help=u"调用合约函数 'function arg1 arg2' -a xxx")
    parser.add_option("-q", "--query", type="string", dest="query", help=u"查询合约数据 'function arg1 arg2' -a xxx")
    parser.add_option("-a", "--contract_address", type="string", dest="contract_address", help=u"调用的合约地址'")
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

    contract_address = options.contract_address
    call = options.call
    if call:
        if not contract_address:
            print red("Please specify -a ")
            return

        _args = call.strip().split(" ")
        function = _args[0]
        if not function:
            print red("function Must Exist")
            return
        result = neb.call(contract_address, function, _args[1:])
        print result
        check_transaction(neb, result['txhash'])

    query = options.query
    if query:
        if not contract_address:
            print red("Please specify -a ")
            return
        _args = query.strip().split(" ")
        function = _args[0]
        if not function:
            print red("function Must Exist")
            return
        print neb.query(contract_address, function, _args[1:])

    txhash = options.txhash
    if txhash:
        check_transaction(neb, txhash)



if __name__ == "__main__":
    main()

