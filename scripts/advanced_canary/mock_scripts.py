from brownie import VRFCoordinatorV2Mock, LinkToken


contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorV2Mock,
    "vrf_link_token": LinkToken,
}


def deploy_mocks(account, contract_name):

    if contract_name == "vrf_coordinator":
        VRFCoordinatorV2Mock.deploy(
            100000,
            100000,
            {"from": account},
        )

        print(
            "A new mock instance for VRFCoordinatorV2 Contract has been created at address:",
            VRFCoordinatorV2Mock[-1].address,
        )
    if contract_name == "vrf_link_token":
        LinkToken.deploy({"from": account})
        print(
            "A new mock instance for LINKToken Contract has been created at address:",
            LinkToken[-1].address,
        )
