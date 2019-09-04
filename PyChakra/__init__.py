# -*- coding: utf-8 -*-
#
#  ___         ___  _           _
# | _ \ _  _  / __|| |_   __ _ | |__ _ _  __ _
# |  _/| || || (__ | ' \ / _` || / /| '_|/ _` |
# |_|   \_, | \___||_||_|\__,_||_\_\|_|  \__,_|
#       |__/
#
# PyChakra is a Python binding to Microsoft Chakra JavaScript engine.

import sys
import json
import platform
from os import path
from ctypes import *

def get_lib_path():
    root = path.dirname(__file__)

    if sys.platform == "darwin":
        return path.join(root, "libs/osx/libChakraCore.dylib")

    if sys.platform.startswith("linux"):
        return path.join(root, "libs/linux/libChakraCore.so")

    if sys.platform == "win32":
        if platform.architecture()[0].startswith("64"):
            return path.join(root, "libs/windows/x64/ChakraCore.dll")
        else:
            return path.join(root, "libs/windows/x86/ChakraCore.dll")

    raise RuntimeError("ChakraCore not support your platform: %s, detail see: https://github.com/Microsoft/ChakraCore",
                       sys.platform)

class JSError(Exception):
    def __init__(self,ErrorInfo):
        super(JSError,self).__init__()
        self.errorinfo = ErrorInfo
    def __str__(self):
        return self.errorinfo


class Runtime:
    def __init__(self):
        self.chakraCore = CDLL(get_lib_path())
        self.__mcode = ["""var replace = function(k,v) {
                if (typeof v === 'function') {
                    return Function.prototype.toString.call(v)
                } else if (v === undefined ) {
                    return null
                } else {
                    return v
                } };"""]
        self.__count = 0
        self.__init_runtime()
        self.__init_context()
        # call DllMain manually on non-Windows
        if sys.platform != "win32":
            # Attach process
            self.chakraCore.DllMain(0, 1, 0)
            # Attach main thread
            self.chakraCore.DllMain(0, 2, 0)

    def __init_runtime(self):
        self.runtime = c_void_p()
        self.chakraCore.JsCreateRuntime(0, 0, byref(self.runtime))
    
    def __init_context(self):
        self.context = c_void_p()
        self.chakraCore.JsCreateContext(self.runtime, byref(self.context))
        self.chakraCore.JsSetCurrentContext(self.context)
    
    def __del__(self):
        # Dispose runtime
        self.chakraCore.JsDisposeRuntime(self.runtime)

    def __get_exception(self):
        exception = c_void_p()
        self.chakraCore.JsGetAndClearException(byref(exception))

        exception_id = c_void_p()
        self.chakraCore.JsCreatePropertyId(b"message", 7, byref(exception_id))

        value = c_void_p()
        self.chakraCore.JsGetProperty(exception, exception_id, byref(value))

        return self.__js_value_to_str(value)
    
    def __js_value_to_str(self,jsResult):
        # Convert script result to String in JavaScript; redundant if script returns a String
        resultJSString = c_void_p()
        self.chakraCore.JsConvertValueToString(jsResult, byref(resultJSString))
        stringLength = c_size_t()
        # Get buffer size needed for the result string
        self.chakraCore.JsCopyString(resultJSString, 0, 0, byref(stringLength))
        resultSTR = create_string_buffer(stringLength.value + 1); # buffer is big enough to store the result
        # Get String from JsValueRef
        self.chakraCore.JsCopyString(resultJSString, byref(resultSTR), stringLength.value + 1, 0)
        # Set `null-ending` to the end
        resultSTRLastByte = (c_char * stringLength.value).from_address(addressof(resultSTR))
        resultSTRLastByte = '\0'
        return resultSTR.value.decode('utf8')

    def eval(self,script):
        self.__count += 1
        if self.__count == 5: # Reset Context Incase exploied
            self.__init_context()
            self.__count = 0

        script = '\n'.join(self.__mcode)+'''\nJSON.stringify(eval(%s),replace);'''%repr(script)
        script = create_string_buffer(script.encode('UTF-16'))
        
        fname = c_void_p()
        # create JsValueRef from filename
        self.chakraCore.JsCreateString("", 0, byref(fname))
        scriptSource = c_void_p()
        # Create ArrayBuffer from script source
        self.chakraCore.JsCreateExternalArrayBuffer(script, len(script), 0, 0, byref(scriptSource))
        jsResult = c_void_p()
        # Run the script.
        err = self.chakraCore.JsRun(scriptSource, 0 , fname, 0x02, byref(jsResult))
        if err == 0:
            return json.loads(self.__js_value_to_str(jsResult))
        # js exception
        elif err == 196609:
            raise JSError(self.__get_exception())
        # other error
        else:
            raise Exception(jsResult)
    
    def set_variable(self,name,value):
        self.eval("var %s = %s" % (name, json.dumps(value)))
        return True

    def get_variable(self,name):
        value = self.eval("JSON.stringify((() => %s)())" % name)
        return json.loads(value)
    
    def require(self,js_file):
        with open(js_file) as f:
            self.__mcode.append(f.read())
    
    def compile(self,script):
        '''Add some function to the context. But not Running, wait for Call.If you want to run it,just eval it.'''
        self.__mcode.append(script)

    def call(self,identifier,*args):
        args = json.dumps(args)
        return self.eval("%s.apply(this, %s)"%(identifier, args))
    
    def call_for_each(self,identifier,*args):
        args = json.dumps(args)
        script = '''function callForEverybody(bodys) { return bodys.map(x => %s(x));}
        callForEverybody.apply(this,%s);'''%(identifier,args)
        return self.eval(script)
