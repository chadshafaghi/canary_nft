from scripts.advanced_canary.canary_advanced_collectible import (
    deploy_advanced_canary_collectible,
    mint_advanced_canary_collectible,
    top_up_subscription_with_link,
    reveal_advanced_canary_collectible_token,
    cancel_subscription,
)
from scripts.helpful_scripts import get_account
from scripts.advanced_canary.vrf_helpful_scripts import (
    fund_contract_with_link,
    withdraw_link_balance,
)


opensea_url = "https://testnets.opensea.io/assets/{}/{}"


def main():

    account = get_account()

    # 1 Canary Advanced NFT token (ERC721) is deployed. It required the Randomness Chainlink manager to geenrate randomness in a decentralized manner
    canary_advanced_collectible = deploy_advanced_canary_collectible(account)

    # 2 Fund Contract with Link and top up subscription
    fund_contract_with_link(account, canary_advanced_collectible)

    # 3 Top up Link for the Subscribee (Smart Contract NFT subscribe to VRF Consumer V2)
    top_up_subscription_with_link(account, canary_advanced_collectible)

    # 4 Canary Advanced NFT can be now minted
    (token_id, mint_tx) = mint_advanced_canary_collectible(
        account, canary_advanced_collectible
    )
    # Get the random chainlink requestID from the mint events
    request_id = mint_tx.events["randomBreedRequest"]["requestId"]
    print(
        f"A New random number has been requested to Chainlink request_id :{request_id}"
    )

    # 5 TokenId can now be revealed. metadata are geenrated
    reveal_advanced_canary_collectible_token(
        account, canary_advanced_collectible, token_id
    )

    # 6 Cancel Subscription and withdraw Link Balance to the owner
    # cancel_subscription(account, canary_advanced_collectible)
    withdraw_link_balance(account, canary_advanced_collectible)
    print(
        "Advanced Canary NFT has been created and a token has been minted with a Random Breed - Thanks ChainLink !"
    )
    print(
        f"The CanaryAdvanced NFT collection is available on OpenSea : {opensea_url.format(canary_advanced_collectible.address,canary_advanced_collectible.tokenCounter())}"
    )
