from scripts.advanced_canary.vrf_randomness_manager import (
    deploy_vrf_randomness_manager,
)
from scripts.advanced_canary.canary_advanced_collectible import (
    deploy_advanced_canary_collectible,
    add_advanced_canary_as_vrf_consumer,
    mint_advanced_canary_collectible,
    reveal_advanced_canary_collectible_token,
)
from scripts.helpful_scripts import get_account

import time

opensea_url = "https://testnets.opensea.io/assets/{}/{}"


def main():

    account = get_account()

    # 1. Randomness Manager Contract is deployed
    vrf_subscriptionManager = deploy_vrf_randomness_manager(account)

    # 2 Camnary Advanced NFT token (ERC721) is deployed. It required the Randomness Chainlink manager to geenrate randomness in a decentralized manner
    canary_advanced_collectible = deploy_advanced_canary_collectible(
        account, vrf_subscriptionManager.address
    )
    # 3 Contract need to be authorized as a Consumer to generate randomNumber.
    add_advanced_canary_as_vrf_consumer(
        account, canary_advanced_collectible, vrf_subscriptionManager
    )
