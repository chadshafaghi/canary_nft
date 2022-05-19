from brownie import config, network, SimpleCanaryCollectible
from scripts.helpful_scripts import get_account, opensea_url

sample_token_uri = (
    "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
)


def main():
    deploy_simple_canary_nft(get_account())


def deploy_simple_canary_nft(from_account):
    simple_canary_collectible = SimpleCanaryCollectible.deploy(
        {"from": from_account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"The NFT Factory has been minted at address:{simple_canary_collectible}")

    tx_mint = simple_canary_collectible.createCollectible(
        sample_token_uri, {"from": from_account}
    )
    tx_mint.wait(1)
    print(
        f"Transaction {tx_mint} completed - The Canary Colectible has been minted. You can see your NFT in OpenSea url {opensea_url.format(simple_canary_collectible.address,simple_canary_collectible.totalSupply())}"
    )

    return simple_canary_collectible
