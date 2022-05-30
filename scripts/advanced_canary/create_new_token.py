from brownie import AdvancedCanaryCollectible
from scripts.helpful_scripts import get_account
from scripts.advanced_canary.canary_advanced_collectible import (
    mint_advanced_canary_collectible,
    reveal_advanced_canary_collectible_token,
    top_up_subscription_with_link,
)
from scripts.advanced_canary.vrf_helpful_scripts import (
    fund_contract_with_link,
    withdraw_link_balance,
)


def main():
    # This script hould be used only in testnet environment as it relies on an existing AdvancedCanaryCollectible[0]

    # 1 Preparation - getting contract instances and funding
    account = get_account()
    contract = AdvancedCanaryCollectible[-1]
    # fund_contract_with_link(account, contract)
    # top_up_subscription_with_link(account, contract)
    token_id, tx_mint = mint_advanced_canary_collectible(account, contract)
    reveal_advanced_canary_collectible_token(account, contract, token_id)

    # we withdraw pending LINK to keep our wallet balance healthy
    # withdraw_link_balance(account, contract)
