from brownie import AdvancedCanaryCollectible
from scripts.helpful_scripts import get_account
from scripts.advanced_canary.canary_advanced_collectible import (
    mint_advanced_canary_collectible,
    reveal_advanced_canary_collectible_token,
)
import time


def main():
    account = get_account()
    canary_advanced_collectible = AdvancedCanaryCollectible[1]

    # 4 Additional Canary Advanced NFT can be now minted
    token_id = mint_advanced_canary_collectible(account, canary_advanced_collectible)

    # Chainlink has now received the request for randomness and is managing the processing asynchronously. In a a Front End we would have manage the UX differently.
    print(f"Waiting for Chainlink to provide randomness....via request")
    time.sleep(180)

    reveal_advanced_canary_collectible_token(
        account, canary_advanced_collectible, token_id
    )

    print("Thanks Chainlink for providing secure randomless - Sincerly Chad ! ")
