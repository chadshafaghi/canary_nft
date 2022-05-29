from scripts.helpful_scripts import get_contract
from web3 import Web3

ETHER = "ether"
LINK_TOKEN_REQUIRED = Web3.toWei(3, ETHER)


def fund_contract_with_link(account, canary_contract):
    vrf_link_token = get_contract("vrf_link_token")

    # Fund Contract with Link
    tx_fund_contract_with_link = vrf_link_token.transfer(
        canary_contract, LINK_TOKEN_REQUIRED, {"from": account}
    )
    tx_fund_contract_with_link.wait(1)
    print(
        f"{Web3.fromWei(LINK_TOKEN_REQUIRED,ETHER)} Link has been funded the Canary Advanced NFT smart contract {canary_contract}.... "
    )


def withdraw_link_balance(account, contract):
    vrf_link_token = get_contract("vrf_link_token")
    balance = vrf_link_token.balanceOf(contract)
    if balance > 0:
        tx_withdraw = contract.withdraw(balance, account, {"from": account})
        tx_withdraw.wait(1)
        print(
            f"Canary Advanced NFT Contract balance of {Web3.fromWei(balance,ETHER)} LINK has been transfered to contract Owner wallet : {account}"
        )
    else:
        print(
            f"No outstanding Link balance within Canary Advanced NFT Contract {contract.address}"
        )
