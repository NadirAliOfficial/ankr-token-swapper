
# 🪙 Ankr Token Swapper (Python)

A lightweight Python utility using `web3.py` to:
- ✅ Check token balance of any ERC-20
- 🔁 Swap ETH to any token (`swap_buy`)
- 🔁 Swap token to ETH (`swap_sell`)

Built to integrate with [Ankr RPC](https://www.ankr.com/rpc/) and Uniswap V2 (or compatible routers like PancakeSwap on BSC).

---

## ⚙️ Requirements

```bash
pip install web3 eth-account
````

---

## 🚀 Setup

1. Clone the repo
2. Replace:

   * `ANKR_RPC` with your chain-specific Ankr endpoint
   * `PRIVATE_KEY` with your wallet's private key
3. Run the script

---

## 🧠 Functions

```python
check_token_balance(token_address)
```

Returns the balance and symbol of a given ERC-20 token.

```python
swap_buy(token_address, eth_amount)
```

Swaps ETH for a token using Uniswap V2 router.

```python
swap_sell(token_address, percentage=100)
```

Swaps held tokens back to ETH.

---

## 🛡️ Disclaimer

> ⚠️ This script signs real transactions. Use on testnets before deploying on mainnet. Keep your private key secure!

---

## 🧑‍💻 Author

Made by [@TeamNAK](https://theteamnak.com) — feel free to fork, improve, and contribute.
