import web3
import json
import pymysql
from web3 import Web3
""" 
https://zhuanlan.zhihu.com/p/476358202
https://blog.csdn.net/matthewwu/article/details/103157901
https://www.learnblockchain.cn/article/4437
https://blog.csdn.net/a6864657/article/details/131384279 # 调用智能合约上的函数
"""


url = "http://127.0.0.1:7545"
trade_address = Web3.to_checksum_address("0x260c8346157447e2aa69385b96d1e270755c0184")######################填写Contract地址

From = Web3.to_checksum_address("0xe524ae3543aef64ff3fbfcaf2419408888ca6153")######################填写from地址


def connect_to_database():  # 连接本地数据库
    global datapassword
    global database
    connection = pymysql.connect(
        host='127.0.0.1', user='root', password='1234', database='db_4'
    )
    return connection

trade_contract_abi = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_videoId",
				"type": "uint256"
			}
		],
		"name": "buyCopyright",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "videoId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "price",
				"type": "uint256"
			}
		],
		"name": "CopyrightListedForSale",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "videoId",
				"type": "uint256"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "description",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "_key",
				"type": "string"
			}
		],
		"name": "CopyrightRegistered",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "videoId",
				"type": "uint256"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "price",
				"type": "uint256"
			}
		],
		"name": "CopyrightSold",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_goodId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_price",
				"type": "uint256"
			}
		],
		"name": "listCopyrightForSale",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "outPermission",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "bool",
				"name": "set",
				"type": "bool"
			}
		],
		"name": "permit",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_description",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_key",
				"type": "string"
			}
		],
		"name": "registerCopyright",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "setPermission",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "Count",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_address",
				"type": "address"
			}
		],
		"name": "getBalance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_videoId",
				"type": "uint256"
			}
		],
		"name": "getdescription",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_videoId",
				"type": "uint256"
			}
		],
		"name": "getKey",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_GoodId",
				"type": "uint256"
			}
		],
		"name": "getprice",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_num",
				"type": "uint256"
			}
		],
		"name": "getVideoInfo",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "GoodsCopyrights",
		"outputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "description",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "price",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "isForSale",
				"type": "bool"
			},
			{
				"internalType": "string",
				"name": "key",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "permission",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
# sc = w3.eth.contract(address=trade_address, abi=trade_contract_abi)
#
def getHex(num):
    num_hex = hex(num).rstrip("L")
    num_hex_str = num_hex if num_hex.startswith("0x") else "0x" + num_hex
    return num_hex_str



def get_good_id(name): # 查询数据库中名为 goods_infomation 的表中的视频信息
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT id FROM goods_information WHERE name = %s"
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    # 关闭游标和数据库连接
    cursor.close()
    connection.close()
    if result:
        return result[0]  # Returning the id
    else:
        return None  # Return None if name not found


def get_id_num():
    # 获取当前最大id值
    connection = connect_to_database()
    cursor = connection.cursor()
    sql = "SELECT MAX(id) AS max_id FROM goods_information"
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result[0]) # 元组
    max_id = result
    connection.close()
    return result[0]


def upload_blockchain_video_onsale(From, good_hash, price, _key):  # 传入合约地址，密钥与私钥地址与商品价格
    # From是用户账户合约部署地址
    id = get_id_num()  # 获取列表中当前商品数量
    w3 = Web3(Web3.HTTPProvider(url))
    sc = w3.eth.contract(address=trade_address, abi=trade_contract_abi)
    sc.functions.setPermission().transact({'from': From})
    sc.functions.registerCopyright(good_hash, _key).transact({'from': From})  # 确定视频注册编号，并注册视频版权，默认不出售，价格为0
    sc.functions.outPermission().transact({'from': From})
    # 设定出售状态与出售价格
    sc.functions.listCopyrightForSale(id, price).transact({'from': From})
    # 更新数据库




def getTrade(From, _id):
    # 执行交易
    w3 = Web3(Web3.HTTPProvider(url))
    sc = w3.eth.contract(address=trade_address, abi=trade_contract_abi)  # 获取合约对象
    price = sc.functions.getprice(_id).call({'from': From})  # 用智能合约中的 getprice 函数，该函数用于获取给定视频的价格。
    price_hex_str = getHex(price)
    # 进行转账
    sc.functions.buyCopyright(_id).transact({'from': From, 'value': price_hex_str})  # 向智能合约发送一个交易，购买 video_id 对应的版权或服务
    # 获取密钥与私钥地址
    key = sc.functions.getKey(_id).call()
    print(f"AES密钥地址为：{key}")
    priviate_key_address = sc.functions.getdescription(_id).call()
    print(f"RSA私钥地址为：{priviate_key_address}")


def getTX_HASH():
    # 获取最新的区块
    w3 = Web3(Web3.HTTPProvider(url))
    latest_block = w3.eth.get_block('latest')
    # 获取最新区块中的交易列表
    transactions = latest_block['transactions']
    # 输出最新交易的哈希
    latest_tx_hash = transactions[0]
    print("Latest transaction hash:", latest_tx_hash.hex())
    return latest_tx_hash.hex()
    # 上传到数据库trade表：


# def judge(From, _id, seller, buyer):
# 	w3 = Web3(Web3.HTTPProvider(url))
# 	sc = w3.eth.contract(address=trade_address, abi=trade_contract_abi)  # 获取合约对象
# 	price = sc.functions.getprice(_id).call({'from': From})  # 用智能合约中的 getprice 函数，该函数用于获取给定视频的价格。
# 	price_hex_str = getHex(price)
# 	sc.functions.judgeback(_id, seller, buyer).transact({'from':From,'value': price_hex_str})



# if __name__ == '__main__':
#     w3 = Web3(Web3.HTTPProvider(url))
#     sc = w3.eth.contract(address=trade_address, abi=trade_contract_abi)
#     good_hash = "32424324"
#     price =1.00
#     price_in_wei = int(price * 10 ** 18)
#     _key = "123456"
#     upload_blockchain_video_onsale(From,good_hash,price_in_wei,_key)
#     _id = 4
    #getTrade(From,_id)
    #judge(From,4, From,"0x57310a6cb991d579b3Dc7159164f1Ac5C98Dea69")


