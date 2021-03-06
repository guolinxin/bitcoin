##########################################################################
#
# Test functionality related to mining
#
# MIT license
#
# Copyright (c) 2018 christianb93
# Permission is hereby granted, free of charge, to 
# any person obtaining a copy of this software and 
# associated documentation files (the "Software"), 
# to deal in the Software without restriction, 
# including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, 
# sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice 
# shall be included in all copies or substantial 
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY 
# OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS 
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
##########################################################################

import docker
import time
import os

import btc.txn
import btc.script
import btc.keys
import btc.utils

import pytest

from fixtures import startEnv


        
#
# Test Miner
#
def test_tc1(startEnv):
    #
    # After setup, we should not have any transactions on this address
    #
    l = btc.utils.rpcCall("listtransactions")
    x = [_ for _ in l if _['address'] == "mpV4bFDWN8NrWX9u3V47UgzxD9wSLQivwj"]
    assert(0 == len(x))
    #
    # Now transfer 1 bitcoin to the address 
    #
    out = os.system("python SendMoney.py")
    time.sleep(1)
    #
    # Find the transaction 
    #
    l = btc.utils.rpcCall("listtransactions")
    x = [_ for _ in l if _['address'] == "mpV4bFDWN8NrWX9u3V47UgzxD9wSLQivwj"]
    assert(1 == len(x))
    _txn = x[0]
    assert(_txn['amount'] == -1.0)
    txid = _txn['txid']
    chaininfo_old = btc.utils.rpcCall("getblockchaininfo")
    #
    # Now run the miner and ask it to mine one block
    #
    out = os.system("python Miner.py")
    time.sleep(1)
    chaininfo_new = btc.utils.rpcCall("getblockchaininfo")
    assert(chaininfo_new['blocks'] == (1 + chaininfo_old['blocks']))
    blockid = chaininfo_new['bestblockhash']
    #
    # Get this block
    #
    block = btc.utils.rpcCall("getblock", [blockid])
    txns = block['tx']
    #
    # Now verify that the transaction generated by SendMoney
    # is in that block at position 2
    #
    assert(2 == len(txns))
    assert(txns[1] == txid)
    
    
    
    
