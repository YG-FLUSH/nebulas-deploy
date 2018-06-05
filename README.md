# nebulas 星云链部署测试

# config

```
config = {
    "domain": "http://localhost:8685",
    "address": "n1FF1nz6tarkDVwWQkMnnwFPuPKUaQTdptE",
    "passphrase": "passphrase",
}
```

# install environment

```
pip install -r requirements.txt
```

# usage

* 部署合约
    ```
    python contract.py -d xxx_contract.js
    {u'txhash': u'26d5e57a79dcc9abf9729672927ac6873a676002f8d943d1dedf610d41288398', u'contract_address': u'n1uW9JZ2H2ys6XoYsSNr9sFDNXn3pDNPD3V'}
    ```

* 调用合约

    ```
    # 调用函数
    python contract.py -c 'function args1 args2' -a contract_address
    # 查询数据
    python contract.py -q 'function args1 args2' -a contract_address
    ```

* 查询交易状态

    ```
        python contract.py -t txhashxxxxx
    ```

