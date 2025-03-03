# PyEvalJS

PyEvalJS is a python wrapper for [Microsoft Chakra](https://github.com/Microsoft/ChakraCore) engine, it act as a bridge between the Python and JavaScript objects, and with this module you can easily run JavaScript Code in Python without having to install nodejs.

## Installation

    pip install PyEvalJS

## Usage

### Execute a script

```python
>>> from PyEvalJS import Runtime
>>> runtime = Runtime()
>>> runtime.eval("'red yellow blue'.split(' ')")
['red', 'yellow', 'blue']
```

### Call a function

```python
>>> from PyEvalJS import Runtime
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
>>> from PyEvalJS import Runtime
>>> runtime = Runtime()
>>> runtime.eval("""
...     function add2(num) {
...         return num+2;
...     } add2(8);""")
10
```

or by passing parameters

```python
>>> from PyEvalJS import Runtime
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
>>> from PyEvalJS import Runtime
>>> runtime = Runtime()
>>> runtime.set_variable("name", ['Jim','Bob','Tour'])
True
>>> runtime.get_variable("name")
['Jim', 'Bob', 'Tour']
```

### Use a JavaScript module

```python
>>> from PyEvalJS import Runtime
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
>>> from PyEvalJS import Runtime
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

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Licence

Code released under [the MIT license](https://github.com/Satireven/PyEvalJS/blob/master/LICENSE)