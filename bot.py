import json
from web3 import Web3
from eth_account import Account

ANKR_RPC = "https://rpc.ankr.com/multichain/f943d482902e1f866767c57053e9e5db3575dd95e27a5e79c68463005b0a0259"
PRIVATE_KEY = "YOUR_PRIVATE_KEY_HERE"  # Replace with your private key
ROUTER_ADDRESS = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"  # Uniswap V2 Router
WETH_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"   # WETH token address


web3 = Web3(Web3.HTTPProvider(ANKR_RPC))
account = Account.from_key(PRIVATE_KEY)
ADDRESS = account.address

# Load router ABI
UNISWAP_ROUTER_ABI = json.loads("""
[
  {
    "name": "swapExactETHForTokens",
    "type": "function",
    "inputs": [
      {"name": "amountOutMin", "type": "uint256"},
      {"name": "path", "type": "address[]"},
      {"name": "to", "type": "address"},
      {"name": "deadline", "type": "uint256"}
    ],
    "outputs": [{"name": "amounts", "type": "uint256[]"}],
    "stateMutability": "payable"
  },
  {
    "name": "swapExactTokensForETH",
    "type": "function",
    "inputs": [
      {"name": "amountIn", "type": "uint256"},
      {"name": "amountOutMin", "type": "uint256"},
      {"name": "path", "type": "address[]"},
      {"name": "to", "type": "address"},
      {"name": "deadline", "type": "uint256"}
    ],
    "outputs": [{"name": "amounts", "type": "uint256[]"}],
    "stateMutability": "nonpayable"
  }
]
""")

router = web3.eth.contract(address=Web3.to_checksum_address(ROUTER_ADDRESS), abi=UNISWAP_ROUTER_ABI)


def check_token_balance(token_address):
    erc20_abi = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "symbol",
            "outputs": [{"name": "", "type": "string"}],
            "type": "function"
        }
    ]
    token = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=erc20_abi)
    balance = token.functions.balanceOf(ADDRESS).call()
    decimals = token.functions.decimals().call()
    symbol = token.functions.symbol().call()
    return f"{balance / 10**decimals:.4f} {symbol}"


def swap_buy(token_address, eth_amount):
    token_address = Web3.to_checksum_address(token_address)
    path = [Web3.to_checksum_address(WETH_ADDRESS), token_address]
    deadline = web3.eth.get_block("latest")["timestamp"] + 1200

    tx = router.functions.swapExactETHForTokens(
        0,  # Accept any amount out
        path,
        ADDRESS,
        deadline
    ).build_transaction({
        "from": ADDRESS,
        "value": web3.to_wei(eth_amount, "ether"),
        "gas": 250000,
        "gasPrice": web3.to_wei("5", "gwei"),
        "nonce": web3.eth.get_transaction_count(ADDRESS)
    })

    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return f"Buy Tx Sent: {web3.to_hex(tx_hash)}"


def swap_sell(token_address, percentage=100):
    token_address = Web3.to_checksum_address(token_address)
    erc20_abi = [
        {
            "constant": False,
            "inputs": [
                {"name": "spender", "type": "address"},
                {"name": "value", "type": "uint256"}
            ],
            "name": "approve",
            "outputs": [{"name": "", "type": "bool"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [{"name": "owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "type": "function"
        }
    ]
    token = web3.eth.contract(address=token_address, abi=erc20_abi)
    balance = token.functions.balanceOf(ADDRESS).call()
    sell_amount = int(balance * percentage / 100)

    # Approve tokens
    approve_tx = token.functions.approve(Web3.to_checksum_address(ROUTER_ADDRESS), sell_amount).build_transaction({
        "from": ADDRESS,
        "gas": 80000,
        "gasPrice": web3.to_wei("5", "gwei"),
        "nonce": web3.eth.get_transaction_count(ADDRESS)
    })
    signed_approve = web3.eth.account.sign_transaction(approve_tx, PRIVATE_KEY)
    web3.eth.send_raw_transaction(signed_approve.rawTransaction)

    # Sell tokens
    path = [token_address, Web3.to_checksum_address(WETH_ADDRESS)]
    deadline = web3.eth.get_block("latest")["timestamp"] + 1200

    sell_tx = router.functions.swapExactTokensForETH(
        sell_amount,
        0,
        path,
        ADDRESS,
        deadline
    ).build_transaction({
        "from": ADDRESS,
        "gas": 250000,
        "gasPrice": web3.to_wei("5", "gwei"),
        "nonce": web3.eth.get_transaction_count(ADDRESS)
    })
    signed_sell = web3.eth.account.sign_transaction(sell_tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_sell.rawTransaction)
    return f"Sell Tx Sent: {web3.to_hex(tx_hash)}"

