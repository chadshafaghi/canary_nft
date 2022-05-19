from brownie import config, network, AdvancedCanaryCollectible


def deploy_advanced_canary_collectible(account, vrf_subscriptionManager):
    canary_advanced_collectible = AdvancedCanaryCollectible.deploy(
        vrf_subscriptionManager,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(
        f"Canary Advanced NFT Contract has been created at address {canary_advanced_collectible.address}"
    )
    return canary_advanced_collectible


def add_advanced_canary_as_vrf_consumer(
    account, canary_advanced_collectible, vrf_subscriptionManager
):
    authorization_tx = vrf_subscriptionManager.addConsumer(
        canary_advanced_collectible.address, {"from": account}
    )
    authorization_tx.wait(1)
    print(
        f"Advanced Canary Token {canary_advanced_collectible} has been added to the list of Consumer authorized to generate randomness."
    )


def mint_advanced_canary_collectible(account, canary_advanced_collectible):
    mint_tx = canary_advanced_collectible.mintCollection({"from": account})
    mint_tx.wait(1)

    token_id = canary_advanced_collectible.tokenCounter()
    print(f"Advanced Canary Token has been minted with Token Id {token_id}")

    return token_id


def reveal_advanced_canary_collectible_token(
    account, canary_advanced_collectible, token_id
):
    tx_revealed = canary_advanced_collectible.revealTokenId(token_id, {"from": account})
    tx_revealed.wait(1)

    print(
        f"Advanced Canary Token {token_id} has been revealed, Breed will be #{canary_advanced_collectible.canaryRandomBreedByTokenID(token_id)}. "
    )
