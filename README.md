# PyChakra

[![Azure Build Status](https://dev.azure.com/zhengrenzhe/All%20Code%20Tests/_apis/build/status/PyChakra?branchName=master)](https://dev.azure.com/zhengrenzhe/All%20Code%20Tests/_build/latest?definitionId=2&branchName=master)
[![Github Build Status](https://github.com/zhengrenzhe/PyChakra/workflows/Test/badge.svg)](https://github.com/zhengrenzhe/PyChakra/actions)
[![LICENSE](https://img.shields.io/github/license/zhengrenzhe/PyChakra.svg)](https://github.com/zhengrenzhe/PyChakra)
[![VERSION](https://img.shields.io/pypi/v/PyChakra.svg)](https://pypi.org/project/PyChakra/)
[![DL](https://img.shields.io/pypi/dm/PyChakra.svg)](https://pypi.org/project/PyChakra/)


PyChakra is a Python binding to [Microsoft Chakra](https://github.com/Microsoft/ChakraCore)(v1.11.11) Javascript engine.

Chakra is a modern JavaScript engine for Microsoft Edge, it support 96% ES6 feature, Complete info see [https://kangax.github.io/compat-table/es6/](https://kangax.github.io/compat-table/es6/)

## Installation

```
pip install PyChakra
```

## Usage
### Execute a script
```python
>>> from PyChakra import Runtime
>>> runtime = Runtime()
>>> runtime.eval("'red yellow blue'.split(' ')")
['red', 'yellow', 'blue']
```

### Call a function
```python
>>> from PyChakra import Runtime
>>> runtime = Runtime()
>>> runtime.compile("""
...     function add(x, y) {
...         return x + y;
...     }
... """)
>>> runtime.call("add",1,2)
3
```
or just put args into the script
```python
>>> from PyChakra import Runtime
>>> runtime = Runtime()
>>> runtime.eval("""
...     function add2(num) {
...         return num+2;
...     } add2(8);""")
10
```
or by passing parameters
```python
>>> from PyChakra import Runtime
>>> runtime = Runtime()
>>> runtime.set_variable("a",8)
True
>>> runtime.eval("""
...     function add2(num) {
...         return num+2;
...     } add2(a);""")
10
```


### Passing parameters
```python
>>> from PyChakra import Runtime
>>> runtime = Runtime()
>>> runtime.set_variable("name", ['Jim','Bob','Tour'])
True
>>> runtime.get_variable("name")
['Jim', 'Bob', 'Tour']
```

### Use a JavaScript module
```python
>>> from PyChakra import Runtime
>>> runtime = Runtime()
>>> runtime.require("./js/crypto-js.js")  #import CryptoJS
>>> runtime.compile("""
...     function encryptByDESModeCBC(key,message) {
...         var keyHex = CryptoJS.enc.Utf8.parse(key);
...         var ivHex = CryptoJS.enc.Utf8.parse(key);
...         encrypted = CryptoJS.DES.encrypt(message, keyHex, {
...                 iv:ivHex,
...                 mode: CryptoJS.mode.CBC,
...                 padding:CryptoJS.pad.Pkcs7
...             }
...         );
...         return encrypted.ciphertext.toString();
...     }""")
>>> runtime.call("encryptByDESModeCBC",'1234','this is a test')
'94b7b0cc2b71165ea067868f595fc03a'
```

### Call the same function for each item in the list
```python
>>> from PyChakra import Runtime
>>> runtime = Runtime()
>>> runtime.compile("""
...     function add2(num) {
...         return num+2;
... }""")
>>> runtime.call_for_each("add2",[1,2,4,6,5])
[3, 4, 6, 8, 7]

```

## Supports

- Python2 >= 2.7
- Python3 >= 3.4

## Platform

- macOS x64
- Linux x64
- Windows x86/x64 (tested on Windows 10 x64, Python 3.7)
