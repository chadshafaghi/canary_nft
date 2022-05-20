from scripts.advanced_canary.vrf_randomness_manager import (
    deploy_vrf_randomness_manager,
)
from scripts.advanced_canary.canary_advanced_collectible import (
    deploy_advanced_canary_collectible,
    add_advanced_canary_as_vrf_consumer,
    mint_advanced_canary_collectible,
    reveal_advanced_canary_collectible_token,
)

from scripts.helpful_scripts import (
    get_account,
    is_local_env,
)
import pytest


def test_can_create_randomness_manager():
    # if not is_local_env:
    #    pytest.skip()

    account = get_account()
    # 1. Randomness Manager Contract is deployed and subscription is added
    vrf_subscriptionManager = deploy_vrf_randomness_manager(account)
    print(
        f"vrf_subscriptionManager.s_subscriptionId() : {vrf_subscriptionManager.s_subscriptionId() }"
    )
    assert vrf_subscriptionManager.s_subscriptionId() > 0
