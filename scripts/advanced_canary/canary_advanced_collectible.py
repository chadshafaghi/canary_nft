from brownie import config, network, AdvancedCanaryCollectible
from scripts.advanced_canary.vrf_helpful_scripts import LINK_TOKEN_REQUIRED, ETHER
from scripts.helpful_scripts import get_contract, is_local_env
from scripts.advanced_canary.canary_collection_create_metadata import generate_metadata
import time
from web3 import Web3


def deploy_advanced_canary_collectible(account):
    vrf_coordinator = get_contract("vrf_coordinator")
    link_token = get_contract("vrf_link_token")

    canary_advanced_collectible = AdvancedCanaryCollectible.deploy(
        vrf_coordinator,
        link_token,
        config["networks"][network.show_active()]["vrf_key_hash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    print(
        f"Canary Advanced NFT Contract has been created at address {canary_advanced_collectible.address}"
    )
    return canary_advanced_collectible


def mint_advanced_canary_collectible(account, canary_advanced_collectible):
    mint_tx = canary_advanced_collectible.mintNewToken({"from": account.address})
    mint_tx.wait(1)

    token_id = canary_advanced_collectible.tokenCounter()
    print(f"A new Advanced Canary NFT has been minted with Token Id {token_id}")

    return token_id, mint_tx


def reveal_advanced_canary_collectible_token(
    account, canary_advanced_collectible, token_id
):
    tx_revealed = None

    if not is_local_env():
        print(
            f"Waiting for Chainlink to execute the fulfillRandomWords() callback function"
        )
        # Waiting for the RequestID to be solved by Chainlink (asyncrhonous
        # Chainlink has now received the request for randomness and is managing the processing asynchronously.
        # In a Front End we would have manage the UX differently.
        tx_revealed = None
        time.sleep(180)
    else:
        # if local environment, we simulate the callback function
        vrf_coordinator = get_contract("vrf_coordinator")
        tx_revealed = vrf_coordinator.fulfillRandomWords(
            canary_advanced_collectible.tokenIdToRequestId(token_id),
            canary_advanced_collectible.address,
            {"from": account},
        )
        tx_revealed.wait(1)
    # We geenrate the metadata so that we can set the token URI
    token_uri = generate_metadata(
        canary_advanced_collectible.canaryRandomBreedByTokenID(token_id),
        token_id,
    )
    tx_set_token_uri = canary_advanced_collectible.setTokenUri(
        token_id, token_uri, {"from": account}
    )
    tx_set_token_uri.wait(1)

    print(
        f"Advanced Canary Token {token_id} has been revealed and Metadata generated, Canary Breed will be #{canary_advanced_collectible.canaryRandomBreedByTokenID(token_id)}. "
    )
    return tx_revealed


def top_up_subscription_with_link(account, contract):
    vrf_coordinator = get_contract("vrf_coordinator")

    if is_local_env():
        tx_top_up = vrf_coordinator.fundSubscription(
            contract.s_subscriptionId(), LINK_TOKEN_REQUIRED
        )
        # This is only for local development as we can't use topup subscription from the contract
    else:
        tx_top_up = contract.topUpSubscription(LINK_TOKEN_REQUIRED, {"from": account})

    tx_top_up.wait(1)
    print(
        f"{Web3.fromWei(LINK_TOKEN_REQUIRED,ETHER)} LINK has been topped up to the subscriptionId  {contract.s_subscriptionId()} .... "
    )
    return tx_top_up


def cancel_subscription(account, canary_advanced_collectible):

    cancel_tx = canary_advanced_collectible.cancelSubscription(
        account, {"from": account}
    )
    cancel_tx.wait(1)
    balance = cancel_tx.events["SubscriptionCanceled"]["amount"]
    subscriptionId = cancel_tx.events["SubscriptionCanceled"]["subId"]

    print(
        f"Advanced Canary Token {canary_advanced_collectible} subscription # {subscriptionId} has been cancelled and {Web3.fromWei(balance,ETHER)} Link has been withdrawn to Contract owner {account.address}"
    )
    return cancel_tx
