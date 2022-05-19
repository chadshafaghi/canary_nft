from brownie import (
    config,
    network,
    RandomnessManager,
    RandomnessManagerMock,
)
from scripts.helpful_scripts import get_contract, is_local_env

# from scripts.advanced_canary.mock_scripts import g
from web3 import Web3

LINK_TOKEN_REQUIRED = Web3.toWei(3, "ether")


def deploy_vrf_randomness_manager(account):
    vrf_coordinator = get_contract("vrf_coordinator")
    vrf_link_token = get_contract("vrf_link_token")

    if is_local_env():
        print(f"A mock version of RandomnessManager is required...")
        vrf_randomness_manager = RandomnessManagerMock.deploy(
            vrf_coordinator,
            vrf_link_token,
            config["networks"][network.show_active()]["vrf_key_hash"],
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "verify", False
            ),
        )
    else:
        vrf_randomness_manager = RandomnessManager.deploy(
            vrf_coordinator,
            vrf_link_token,
            config["networks"][network.show_active()]["vrf_key_hash"],
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "verify", False
            ),
        )

    print(
        f"The Subscription Manager has been deployed at address:{vrf_randomness_manager}"
    )

    # Fund Contract with Link
    tx_fund_contract_with_link = vrf_link_token.transfer(
        vrf_randomness_manager, LINK_TOKEN_REQUIRED, {"from": account}
    )

    # Top up Subscribee with Link

    tx_fund_contract_with_link.wait(1)
    print(
        f"{LINK_TOKEN_REQUIRED} Link has been funded to the Subscription Manager contract .... "
    )

    tx_fund_link = vrf_randomness_manager.topUpSubscription(
        LINK_TOKEN_REQUIRED, {"from": account}
    )
    tx_fund_link.wait(1)
    print(
        f"{LINK_TOKEN_REQUIRED} LINK has been funded from Subscription Manager {vrf_randomness_manager} contract to the Subscribee {account} .... "
    )

    return vrf_randomness_manager
