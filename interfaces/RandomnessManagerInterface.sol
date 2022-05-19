// SPDX-License-Identifier: MIT
// An example of a consumer contract that also owns and manages the subscription
pragma solidity ^0.8.0;

interface RandomnessManagerInterface {
    function requestRandomWords() external returns (uint256);

    // function fulfillRandomWords(uint256, uint256[] memory randomWords);

    // function createNewSubscription();

    function topUpSubscription(uint256 amount) external;

    function addConsumer(address consumerAddress) external;

    function removeConsumer(address consumerAddress) external;

    function cancelSubscription(address receivingWallet) external;

    function withdraw(uint256 amount, address to) external;

    function getRandomWords() external returns (uint256);
}
