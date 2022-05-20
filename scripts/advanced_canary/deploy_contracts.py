from scripts.advanced_canary.vrf_randomness_manager import (
    deploy_vrf_randomness_manager,
)
from scripts.advanced_canary.canary_advanced_collectible import (
    deploy_advanced_canary_collectible,
    add_advanced_canary_as_vrf_consumer,
    mint_advanced_canary_collectible,
    reveal_advanced_canary_collectible_token,
)
from scripts.helpful_scripts import get_account, is_local_env

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

    # 4 Canary Advanced NFT can be now minted
    token_id = mint_advanced_canary_collectible(account, canary_advanced_collectible)

    # Chainlink has now received the request for randomness and is managing the processing asynchronously. In a a Front End we would have manage the UX differently.
    print(
        f"Waiting for Chainlink to provide randomness....via request {vrf_subscriptionManager.s_requestId()}"
    )

    if not is_local_env():
        time.sleep(180)

    reveal_advanced_canary_collectible_token(
        account, canary_advanced_collectible, token_id
    )

    print("Thanks Chainlink for providing secure randomless - Sincerly Chad ! ")
