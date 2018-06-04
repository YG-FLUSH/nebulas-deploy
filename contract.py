#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   Author: Yoge
#   Time: 2018/06/04

from nebulas import Nebulas
from config import config
from optparse import OptionParser
import time
from huepy import red


def main():
    parser = OptionParser()
    parser.add_option("-d", "--deploy", type="string", dest="contract_file", help=u"部署合约")
    parser.add_option("-c", "--call", type="string", dest="callfunction", help=u"调用合约函数 'contract_address function arg1 arg2'")
    neb = Nebulas(config['domain'], config['address'], config['passphrase'])
    options, _ = parser.parse_args()

    contract_file = options.contract_file
    if contract_file:
        with open(contract_file) as f:
            contract = f.read()
        result = neb.deploy_contract(contract)
        print result
        time.sleep(15)
        print neb.check_transaction(result['txhash'])

    callfunction = options.callfunction
    if callfunction:
        _args = callfunction.split(" ")
        if len(_args) < 2:
            print red("call function should have at lease two args")
            return
        _args.reverse()
        contract_address, function = _args.pop(), _args.pop()
        print neb.call_function(contract_address, function, _args)


if __name__ == "__main__":
    main()

