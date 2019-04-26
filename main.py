from web3 import Web3
import datetime


#web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/34af86e47c754e89bcbf63995a720ade", request_kwargs={'timeout': 60}))
web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/34af86e47c754e89bcbf63995a720ade", request_kwargs={'timeout': 60}))


def scan_transactions(start_block):
    end_block = web3.eth.blockNumber

    wallets_database = []

    for idx in range(start_block, end_block):
        print('Fetching block %d, remaining: %d, progress: %d%%' % (
            idx, (end_block - idx), 100 * (idx - start_block) / (end_block - start_block)))

        block = web3.eth.getBlock(idx, full_transactions=True)
        counter = 0
        for tx in block.transactions:
            if tx['to'] is not None and tx['to'] not in wallets_database:
                counter += 1
                wallets_database.append(tx['to'])
            if tx['from'] is not None and tx['from'] not in wallets_database:
                counter += 1
                wallets_database.append(tx['from'])
        print('New wallets:', counter)
    return wallets_database


wallets_database = scan_transactions(0)
print(len(wallets_database))
wallets_with_balance = []
total_balances = 0
for wallet in wallets_database:
    balance = web3.fromWei(web3.eth.getBalance(wallet), 'ether')
    if balance > 0:
        print(wallet, balance)
        wallets_with_balance.append(wallet)
        total_balances += balance

print(len(wallets_with_balance))
print('Average Balance:', total_balances / len(wallets_with_balance))
