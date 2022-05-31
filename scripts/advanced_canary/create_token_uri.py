from brownie import network, AdvancedCanaryCollectible
from scripts.helpful_scripts import get_account
from scripts.advanced_canary.canary_collection_create_metadata import generate_metadata

# This script will look at all tokens created for the last deployed contract
# and will geenrate corresponding token URI in case they have been missed
def main():
    contract = AdvancedCanaryCollectible[-1]
    account = get_account()
    for token_id in range(1, contract.tokenCounter() + 1):
        if not contract.tokenURI(token_id, {"from": account}).startswith("https"):
            print(f"Token ID# {token_id} is missing token URI")
            token_uri = generate_metadata(
                contract.tokenIdToCanaryRandomBreed(token_id), token_id
            )
            print(
                f"Token URI for Token ID {token_id} has been geenreated : {token_uri}"
            )
            # we now need to set in the contract the token
            tx_set_token_uri = contract.setTokenUri(
                token_id, token_uri, {"from": account}
            )
            tx_set_token_uri.wait(1)
            print(
                f"Token URI for Token ID {token_id} has been published to the contract {contract.address} "
            )
