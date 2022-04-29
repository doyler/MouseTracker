from concurrent.futures.thread import ThreadPoolExecutor
from dotenv import load_dotenv
import os
import requests
import json
import sys
from web3 import Web3

# Get Environment Variables
load_dotenv()
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
# Can also use Infura, but Alchemy is slightly better at the free tier
WEB3_URL = os.getenv('ALCHEMY_URL')

ABI_ENDPOINT = 'https://api.etherscan.io/api?module=contract&apikey=%s&action=getabi&address='%(ETHERSCAN_API_KEY)

# Setting up the HTTP requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'Accept': 'application/json'
}
session = requests.Session()
session.headers.update(headers)

# Setting up web3 stuff
web3 = Web3(Web3.HTTPProvider(WEB3_URL))


# These are some constants for the examples below,
# hopefully it demonstrates checking staking/non-staking contracts.

# Anonymice Contract - https://etherscan.io/address/0xbad6186e92002e312078b5a1dafd5ddf63d3f731#code
MOUSE_ADDRESS = '0xbad6186e92002e312078b5a1dafd5ddf63d3f731'
# Cheeth Contract - https://etherscan.io/address/0x5f7ba84c7984aa5ef329b66e313498f0aed6d23a#code
CHEETH_ADDRESS = '0x5f7ba84c7984aa5ef329b66e313498f0aed6d23a'
# Baby Contract - https://etherscan.io/address/0x15cc16bfe6fac624247490aa29b6d632be549f00#code
BABY_ADDRESS = '0x15cc16bfe6fac624247490aa29b6d632be549f00'

# FOMO Contract - https://etherscan.io/address/0x818a19a6d3f0859b68e8490a6e945a51060caad1#code
FOMO_ADDRESS = '0x818a19a6d3f0859b68e8490a6e945a51060caad1'

# Habibz Contract - https://etherscan.io/address/0x98a0227e99e7af0f1f0d51746211a245c3b859c2#code
HABIBZ_ADDRESS = '0x98a0227e99e7af0f1f0d51746211a245c3b859c2'

# WarKittens Contract - https://etherscan.io/address/0xC4771c27FB631FF6046845d06561bF20eF753DaB#code
WK_ADDRESS = '0xc4771c27fb631ff6046845d06561bf20ef753dab'

# Set the target project information here
TARGET_CONTRACT = WK_ADDRESS
TARGET_NAME = "War Kittens"

# In theory this should be obtained from the totalSupply()
MAX_SUPPLY = 9500.0

# These sections are if you want to include staking logic.
# If not, you only need one of these methods
#######################################################################################################
abi_mice_contract = requests.get('%s%s'%(ABI_ENDPOINT, MOUSE_ADDRESS)).json()['result']
address_mice = Web3.toChecksumAddress(MOUSE_ADDRESS)
mice_contract = web3.eth.contract(address=address_mice, abi=abi_mice_contract)

abi_cheeth_contract = requests.get('%s%s'%(ABI_ENDPOINT, CHEETH_ADDRESS)).json()['result']
address_cheeth = Web3.toChecksumAddress(CHEETH_ADDRESS)
cheeth_contract = web3.eth.contract(address=address_cheeth, abi=abi_cheeth_contract)

abi_baby_contract = requests.get('%s%s'%(ABI_ENDPOINT, BABY_ADDRESS)).json()['result']
address_baby = Web3.toChecksumAddress(BABY_ADDRESS)
baby_contract = web3.eth.contract(address=address_baby, abi=abi_baby_contract)
#######################################################################################################

# Here is the example if you only want to check FROM one contract.
#abi_source_contract = requests.get('%s%s'%(ABI_ENDPOINT, HABIBZ_ADDRESS)).json()['result']
#address_source = Web3.toChecksumAddress(HABIBZ_ADDRESS)
#source_contract = web3.eth.contract(address=address_source, abi=abi_source_contract)

abi_tgt_contract = requests.get('%s%s'%(ABI_ENDPOINT, TARGET_CONTRACT)).json()['result']
address_tgt = Web3.toChecksumAddress(TARGET_CONTRACT)
tgt_contract = web3.eth.contract(address=address_tgt, abi=abi_tgt_contract)

# Don't change this, definitely breaks everything!
doyler_address = '0xeD19c8970c7BE64f5AC3f4beBFDDFd571861c3b7'

all_owners = set()

# Again, these variables are only needed if you want to check holders of
# "multiple" different collections/wallets
#######################################################################################################
mouse_owners = []
staked_mice = []
staked_mice_owners = []
burned_mice_owners = []
baby_mice_owners = []
#######################################################################################################

# Example variable for 1:1 checking
# source_owners = []

tgt_counts = {}

# More mouse specific examples
# "multiple" different collections/wallets
#######################################################################################################
def getMiceOwners(tokenID):
    owner = mice_contract.functions.ownerOf(tokenID).call()
    #owner = owner.lower()
    
    # Technically ETH addresses are case-insensitive, but saw a few weird cases with dEaD in particular
    # 0x000000000000000000000000000000000000dEaD  -  Anonymice burned
    # 0x5f7BA84c7984Aa5ef329B66E313498F0aEd6d23A  -  Cheeth v1 staked
    if owner.lower() == "0x000000000000000000000000000000000000dead".lower():
        burned_mice_owners.append(owner)
    elif owner.lower() == "0x5f7BA84c7984Aa5ef329B66E313498F0aEd6d23A".lower():
        staked_mice.append(tokenID)
    else:
        mouse_owners.append(owner)

def getBabyOwner(tokenID):
    owner = baby_contract.functions.ownerOf(tokenID).call()
    
    baby_mice_owners.append(owner)
    
def getStakedOwner(tokenID):
    owner = cheeth_contract.functions.getStaker(tokenID).call()
    
    staked_mice_owners.append(owner)
#######################################################################################################    

# Here is the example if you only want to check FROM one contract.
#def getSourceOwner(tokenID):
#    owner = source_contract.functions.ownerOf(tokenID).call()
#    
#    source_owners.append(owner)
    
def addTgtCount(address):
    count = tgt_contract.functions.balanceOf(address).call()
    
    tgt_counts[address] = tgt_counts.get(address, 0) + count

# Parallelize for speed
processes = []

# More mouse specific examples
#######################################################################################################
with ThreadPoolExecutor(max_workers=20) as executor:
    # 10k Genesis mice
    for i in range(0, 10001):
        processes.append(executor.submit(getMiceOwners, i))
        
with ThreadPoolExecutor(max_workers=20) as executor:
    # 3550 babies
    for i in range(0, 3551):
        processes.append(executor.submit(getBabyOwner, i))
        
with ThreadPoolExecutor(max_workers=20) as executor:
    for staked in staked_mice:
        processes.append(executor.submit(getStakedOwner, staked))
        
for owner in mouse_owners:
    all_owners.add(owner)
    
for owner in staked_mice_owners:
    all_owners.add(owner)
    
for owner in baby_mice_owners:
    all_owners.add(owner)
#######################################################################################################

# Here is the example if you only want to check FROM one contract.
#with ThreadPoolExecutor(max_workers=20) as executor:
#    for i in range(0, 10001):
#        processes.append(executor.submit(getSourceOwner, i))
        
#for owner in source_owners:
#    all_owners.add(owner)

with ThreadPoolExecutor(max_workers=20) as executor:
    for owner in all_owners:
        processes.append(executor.submit(addTgtCount, owner))

# More mouse specific examples
#######################################################################################################
mouse_count = 0
staked_count = 0
baby_count = 0
total_count = 0

for owner in mouse_owners:
    if owner in tgt_counts:
        mouse_count += tgt_counts[owner]
    
for owner in staked_mice_owners:
    if owner in tgt_counts:
        staked_count += tgt_counts[owner]    
    
for owner in baby_mice_owners:
    if owner in tgt_counts:
        baby_count += tgt_counts[owner]
#######################################################################################################        
    
for owner in all_owners:
    if owner in tgt_counts:
        total_count += tgt_counts[owner]
    
percentage_owned = total_count / MAX_SUPPLY

print()

print("Anonymice holders (non-staked) currently hold: " + str(mouse_count) + " " + str(TARGET_NAME) + " (non-unique counting)")
print()

print("STAKED mice holders currently hold: " + str(staked_count) + " " + str(TARGET_NAME) + " (non-unique counting)")
print()

print("Baby Anonymice holders currently hold: " + str(baby_count) + " " + str(TARGET_NAME) + " (non-unique counting)")
print()

print()
print("IN TOTAL")
print("=======================================")
print("ALL Unique Anonymice + baby holders have: " + str(total_count) + " " + str(TARGET_NAME))
print("This represents a " + str("{:.2%}".format(percentage_owned)) + " mouse share in the " + str(TARGET_NAME) + " project!!!")
print()

print("Doyler, the dev who wrote this, accepts donations here: " + str(doyler_address))
print()
