# Ankr Token Swapper

A lightweight Python utility that swaps tokens on Ethereum-compatible networks using the Uniswap V2 router via an Ankr RPC endpoint.

## Features
- Token swap via Uniswap/PancakeSwap router
- Ankr RPC endpoint integration
- Slippage protection
- Transaction receipt logging

## Requirements
```
pip install web3 python-dotenv
```

## Configuration
```
ANKR_RPC_URL=https://rpc.ankr.com/eth/your_key
PRIVATE_KEY=your_wallet_private_key
```

## Usage
```bash
python bot.py --from USDC --to ETH --amount 100
```

## Project Structure
```
README.md          # This documentation
LICENSE            # MIT license
bot.py             # Main script implementing swap logic
```

## License
MIT
<!-- updated: 2026-06-18 -->
