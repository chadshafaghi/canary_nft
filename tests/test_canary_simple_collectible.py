from scripts.simple_canary.deploy_and_create import deploy_simple_canary_nft
from scripts.helpful_scripts import (
    get_account,
    is_local_env,
)
import pytest


def test_can_create_simple_canary_collectible():
    if not is_local_env:
        pytest.skip()

    account = get_account()
    simple_canary_collectible = deploy_simple_canary_nft(account)

    assert simple_canary_collectible.totalSupply() > 0
    assert simple_canary_collectible.ownerOf(1) == account
