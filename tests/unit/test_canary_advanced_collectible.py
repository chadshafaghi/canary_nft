from scripts.helpful_scripts import get_contract
from scripts.advanced_canary.vrf_helpful_scripts import (
    fund_contract_with_link,
    withdraw_link_balance,
    LINK_TOKEN_REQUIRED,
)
from scripts.advanced_canary.canary_advanced_collectible import (
    deploy_advanced_canary_collectible,
    mint_advanced_canary_collectible,
    reveal_advanced_canary_collectible_token,
    top_up_subscription_with_link,
    cancel_subscription,
)

from scripts.helpful_scripts import (
    get_account,
    is_local_env,
)
import pytest


def test_can_create_randomness():
    if not is_local_env():
        pytest.skip()

    # Preparation
    account = get_account()

    # Act
    contract = deploy_advanced_canary_collectible(account)

    # Verify that a subscription has been added
    assert contract.s_subscriptionId() > 0


def test_can_mint_new_token():
    if not is_local_env():
        pytest.skip()

    # Preparation
    account = get_account()
    contract = deploy_advanced_canary_collectible(account)

    # Act
    token_id, mint_tx = mint_advanced_canary_collectible(account, contract)
    request_id = mint_tx.events["randomBreedRequest"]["requestId"]

    # Verify that a subscription has been added
    assert token_id > 0
    assert request_id > 0
    assert contract.tokenIdToRequestId(token_id) == request_id
    assert contract.requestIdToTokenId(request_id) == token_id
    assert contract.requestIdToSender(request_id) == account


def test_fund_contract_with_link():
    if not is_local_env():
        pytest.skip()

    # Preparation
    account = get_account()
    contract = deploy_advanced_canary_collectible(account)
    vrf_link_token = get_contract("vrf_link_token")

    # Act
    fund_contract_with_link(account, contract)

    # Assert
    assert vrf_link_token.balanceOf(contract.address) > 0

    # cancel subscription and withdraw LINK balance is required to keep our LINK balance healthy.
    withdraw_link_balance(account, contract)


def test_top_up_subscription_with_link():
    if not is_local_env():
        pytest.skip()

    # Preparation
    account = get_account()
    contract = deploy_advanced_canary_collectible(account)
    vrf_coordinator = get_contract("vrf_coordinator")
    fund_contract_with_link(account, contract)

    # Act
    tx_top_up = vrf_coordinator.fundSubscription(
        contract.s_subscriptionId(), LINK_TOKEN_REQUIRED
    )
    tx_top_up.wait(1)
    subscription_id = tx_top_up.events["SubscriptionFunded"]["subId"]
    old_balance = tx_top_up.events["SubscriptionFunded"]["oldBalance"]
    new_balance = tx_top_up.events["SubscriptionFunded"]["newBalance"]

    assert subscription_id == contract.s_subscriptionId()
    assert old_balance + LINK_TOKEN_REQUIRED == new_balance

    withdraw_link_balance(account, contract)


def test_can_reveal_new_token():
    if not is_local_env():
        pytest.skip()

    # Preparation
    account = get_account()
    contract = deploy_advanced_canary_collectible(account)
    fund_contract_with_link(account, contract)
    top_up_subscription_with_link(account, contract)

    token_id, mint_tx = mint_advanced_canary_collectible(account, contract)
    request_id = mint_tx.events["randomBreedRequest"]["requestId"]

    # Act
    reveal_tx = reveal_advanced_canary_collectible_token(account, contract, token_id)
    reveal_request_id = reveal_tx.events["randomBreedAssigned"]["requestId"]
    random_number = reveal_tx.events["randomBreedAssigned"]["randomNumber"]

    withdraw_link_balance(account, contract)

    # Verify that a subscription has been added
    assert contract.tokenIdToCanaryRandomBreed(token_id) == random_number
    assert request_id == reveal_request_id
    assert random_number > 0
    assert len(contract.tokenIdToTokenURI(token_id)) > 0


def test_cancel_subscription():
    if not is_local_env():
        pytest.skip()

    # Preparation
    vrf_coordinator = get_contract("vrf_coordinator")
    account = get_account()
    contract = deploy_advanced_canary_collectible(account)
    fund_contract_with_link(account, contract)
    top_up_subscription_with_link(account, contract)

    (token_id, tx) = mint_advanced_canary_collectible(account, contract)
    reveal_advanced_canary_collectible_token(account, contract, token_id)

    # Act
    cancel_subscription(account, contract)
    withdraw_link_balance(account, contract)

    assert (
        vrf_coordinator.consumerIsAdded(contract.s_subscriptionId(), contract.address)
        == False
    )
