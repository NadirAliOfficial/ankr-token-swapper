# Ankr Token Swapper

Lightweight Python utility for token swaps via Ankr RPC — interacts with DEX contracts directly.

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
python swap.py --from USDC --to ETH --amount 100
```

## License
MIT
<!-- updated: 2023-07-09-r01 -->
