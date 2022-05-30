from web3 import Web3
from brownie import network, AdvancedCanaryCollectible
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


def test_can_create_smart_contract():
    network.priority_fee("2 gwei")

    if is_local_env():
        pytest.skip()

    # Preparation
    account = get_account()

    # Act
    contract = deploy_advanced_canary_collectible(account)

    # Verify that a subscription has been added and contract address not null
    assert contract.s_subscriptionId() > 0
    assert contract.address != None
    assert contract.symbol() == "aCAN"
    assert contract.tokenCounter() == 0


def test_fund_contract_with_link():
    if is_local_env():
        pytest.skip()

    # Preparation
    account = get_account()
    contract = AdvancedCanaryCollectible[-1]

    vrf_link_token = get_contract("vrf_link_token")

    # Act
    fund_contract_with_link(account, contract)

    # Assert
    assert vrf_link_token.balanceOf(contract.address) == LINK_TOKEN_REQUIRED

    # Transfer LINK balance back to Contract Owner wallet
    withdraw_link_balance(account, contract)


def test_top_up_subscription_with_link():
    if is_local_env():
        pytest.skip()

    # Preparation
    account = get_account()
    contract = AdvancedCanaryCollectible[-1]
    fund_contract_with_link(account, contract)

    # Act
    tx_top_up = top_up_subscription_with_link(account, contract)

    subscription_id = tx_top_up.events["SubscriptionFunded"]["subId"]
    old_balance = tx_top_up.events["SubscriptionFunded"]["oldBalance"]
    new_balance = tx_top_up.events["SubscriptionFunded"]["newBalance"]

    assert subscription_id == contract.s_subscriptionId()
    assert old_balance + LINK_TOKEN_REQUIRED == new_balance

    # we withdraw pending LINK to keep our wallet balance healthy
    withdraw_link_balance(account, contract)


def test_can_mint_new_token():
    if is_local_env():
        pytest.skip()

    # 1 Preparation
    account = get_account()
    contract = AdvancedCanaryCollectible[-1]
    fund_contract_with_link(account, contract)
    top_up_subscription_with_link(account, contract)

    # Act
    (token_id, mint_tx) = mint_advanced_canary_collectible(account, contract)
    request_id = mint_tx.events["randomBreedRequest"]["requestId"]

    # we withdraw pending LINK to keep our wallet balance healthy
    withdraw_link_balance(account, contract)

    # Verify that a subscription has been added
    assert token_id > 0
    assert request_id > 0
    assert contract.tokenIdToRequestId(token_id) == request_id
    assert contract.requestIdToTokenId(request_id) == token_id
    assert contract.requestIdToSender(request_id) == account


def test_can_reveal_new_token():
    if is_local_env():
        pytest.skip()

    # 1 Preparation - getting contract instances and funding
    account = get_account()
    contract = AdvancedCanaryCollectible[-1]
    fund_contract_with_link(account, contract)
    top_up_subscription_with_link(account, contract)
    token_id, tx_mint = mint_advanced_canary_collectible(account, contract)

    # Act
    reveal_advanced_canary_collectible_token(account, contract, token_id)

    # Verify that the Token Breed has been assigned randomly and corresponding Metadata geenrated
    assert contract.tokenIdToCanaryRandomBreed(token_id) > 0
    assert len(contract.tokenIdToTokenURI(token_id)) > 0

    # we withdraw pending LINK to keep our wallet balance healthy
    withdraw_link_balance(account, contract)


def test_cancel_subscription():
    if is_local_env():
        pytest.skip()

    # 1 Preparation - getting contract instances
    account = get_account()
    vrf_link_token = get_contract("vrf_link_token")
    contract = AdvancedCanaryCollectible[-1]

    previous_balance_account = vrf_link_token.balanceOf(account)

    # Act
    tx_cancel = cancel_subscription(account, contract)
    amount_transfer = tx_cancel.events["SubscriptionCanceled"]["amount"]
    withdraw_link_balance(account, contract)

    assert contract.s_subscriptionId() == 0
    assert vrf_link_token.balanceOf(account) == (
        previous_balance_account + amount_transfer
    )
