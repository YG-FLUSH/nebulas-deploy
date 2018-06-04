#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   Author: Yoge
#   Time: 2018/06/04

from nebulas import Nebulas
from config import config
from optparse import OptionParser
import time


def main():
    parser = OptionParser()
    parser.add_option("-d", "--deploy", type="string", dest="contract_file", help=u"部署合约")
    neb = Nebulas(config['domain'], config['address'], config['passphrase'])
    options, _ = parser.parse_args()
    contract_file = options.contract_file
    with open(contract_file) as f:
        contract = f.read()
    result = neb.deploy_contract(contract)
    print result
    time.sleep(15)
    print neb.check_transaction(result['txhash'])



if __name__ == "__main__":
    main()

