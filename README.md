# MouseTracker
Tracks how much of a particular project is owned by mice (genesis, staked, and babies).

This started out as a joke for people to counter-trade mice, but it is useful for tracking and examples in general. 

## Requirements

* Requires Python3+
* Everything in requirements.txt

## Installation

After installing Python 3, just run:

`pip install -r requirements.txt`

## Usage

1. Set your .env variables for ETHERSCAN_API_KEY and WEB3_URL
2. Ensure that the contract address(es) and TARGET_\* variables are correct
3. Run MouseTracker.py

## Example Output

Here is an example run of [Anonymice](https://opensea.io/collection/anonymice) (using only $CHEETH v1) holdings in [WarKittens](https://opensea.io/collection/warkittens).

```
Anonymice holders (non-staked) currently hold: 254 War Kittens (non-unique counting)

STAKED mice holders currently hold: 61 War Kittens (non-unique counting)

Baby Anonymice holders currently hold: 3886 War Kittens (non-unique counting)


IN TOTAL
=======================================
ALL Unique Anonymice + baby holders have: 1260 War Kittens
This represents a 13.26% mouse share in the War Kittens project!!!

Doyler, the dev who wrote this, accepts donations here: 0xeD19c8970c7BE64f5AC3f4beBFDDFd571861c3b7
```

## TODO

* Add support for a Discord bot (or just turn it into one)
* Allow for user input for the target project/contract
* Parse OS URL for the target?
* Better commenting and documentation
* Front-end support and tracking
* Get MAX_SUPPLY from the contract(s)
* Anything else?

# Donations

Doyler is definitely bad at JPEGs, so drop donos here:

`0xeD19c8970c7BE64f5AC3f4beBFDDFd571861c3b7`

Or, hire him - [@NftDoyler](https://twitter.com/NftDoyler)
