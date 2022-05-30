// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

import "@chainlink/contracts/src/v0.8/interfaces/LinkTokenInterface.sol";

import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract AdvancedCanaryCollectible is
    ERC721,
    ERC721URIStorage,
    VRFConsumerBaseV2
{
    using Counters for Counters.Counter;
    enum CanaryBreed {
        DOCTOR,
        GOLDEN,
        KNIGHT,
        LOVE,
        MUSHROOM,
        PHOENIX,
        PUNK,
        RICH,
        TECHRAVE,
        WITCH
    }

    // All those parameters are used to support VRFCOnsumerBaseV2 and provide randomness

    VRFCoordinatorV2Interface COORDINATOR;
    LinkTokenInterface LINKTOKEN;

    //address vrf_coordinator;
    //address vrf_link_token_contract;
    bytes32 vrf_keyHash;

    // The gas lane to use, which specifies the maximum gas price to bump to.
    // A reasonable default is 100000, but this value could be different
    // on other networks.
    uint32 callbackGasLimit = 100000;

    // The default is 3, but you can set this higher.
    uint16 requestConfirmations = 3;

    // Cannot exceed VRFCoordinatorV2.MAX_NUM_WORDS.
    uint32 numWords = 1;

    // Storage parameters
    uint256[] public s_randomWords;
    uint256 public s_requestId;
    uint64 public s_subscriptionId;

    // Mappings and events used to store randomness against each tokenId in the Colletion

    mapping(uint256 => uint256) public tokenIdToRequestId; //Store the random requestId for each tokenId
    mapping(uint256 => uint256) public requestIdToTokenId; //Store the random tokenId for each requesId
    mapping(uint256 => address) public requestIdToSender; //Store the sender address for each requesId

    mapping(uint256 => uint256) public tokenIdToCanaryRandomBreed; //Store the Breed identified for one tokenId. Breed are goin from 1 to 10. 0 is not allowed

    mapping(uint256 => string) public tokenIdToTokenURI; //Store the JSON TokenURI geenrated for this TokenId

    event randomBreedRequest(uint256 indexed requestId, uint256 tokenId);
    event randomBreedAssigned(uint256 indexed requestId, uint256 randomNumber);
    event tokenMetadataGenerated(uint256 indexed tokenId, string tokenUri);

    Counters.Counter public tokenCounter;

    string nftName = "Canary Land NFT Collection";
    string nftSymbol = "aCAN";
    uint256 _numberBreed = 10;

    address s_owner;

    constructor(
        address _vrf_coordinator,
        address _vrf_link_token_contract,
        bytes32 _vrf_keyHash
    ) ERC721(nftName, nftSymbol) VRFConsumerBaseV2(_vrf_coordinator) {
        // initialising VRF coordinator and required configuration to generate randomness
        vrf_keyHash = _vrf_keyHash;

        s_owner = msg.sender;

        COORDINATOR = VRFCoordinatorV2Interface(_vrf_coordinator);
        LINKTOKEN = LinkTokenInterface(_vrf_link_token_contract);

        //Create a new subscription when you deploy the contract.
        createNewSubscription();
    }

    /* 
    @Dev Descrition
    @Dev args : none
    #Dec Returns: tokenId that has just been minted.
    */
    function mintNewToken() public onlyOwner returns (uint256) {
        tokenCounter.increment();
        _safeMint(msg.sender, tokenCounter.current());

        // a random number is requested to the VRF Randomness manager and stored against the token ID.
        s_requestId = COORDINATOR.requestRandomWords(
            vrf_keyHash,
            s_subscriptionId,
            requestConfirmations,
            callbackGasLimit,
            numWords
        );
        // the process of getting a random number is asynchronously completed by chainlink. Once chainlink has completed the randomisation request for requestId,
        // Chainlinlink will then call back fulfillRandomWords() in the RandomnessManager contract. The random numnber will be stored in randomManager._s_randomWords[0]

        tokenIdToRequestId[tokenCounter.current()] = s_requestId;
        requestIdToTokenId[s_requestId] = tokenCounter.current();
        requestIdToSender[s_requestId] = msg.sender;

        emit randomBreedRequest(s_requestId, tokenCounter.current());
    }

    function canaryRandomBreedByTokenID(uint256 tokenId)
        public
        view
        returns (uint256)
    {
        require(
            tokenIdToCanaryRandomBreed[tokenId] > 0,
            "There is no random breed for the given Token Id"
        );
        return tokenIdToCanaryRandomBreed[tokenId];
    }

    modifier onlyOwner() {
        require(
            msg.sender == s_owner,
            "Only Contract owner can execute this transaction"
        );
        _;
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        // leveraging modifier from ERC721 standard EIP implementation
        require(
            _isApprovedOrOwner(msg.sender, tokenId),
            "Only Approved or Owner account can set Canary NFT Metadata (Eg. setTokenURI)"
        );
        return super.tokenURI(tokenId);
    }

    function _burn(uint256 tokenId)
        internal
        override(ERC721, ERC721URIStorage)
    {
        super._burn(tokenId);
    }

    // Create a new subscription when the contract is initially instantiated.
    function createNewSubscription() private onlyOwner {
        // Create a subscription with a new subscription ID.
        address[] memory consumers = new address[](1);
        consumers[0] = address(this);
        s_subscriptionId = COORDINATOR.createSubscription();
        // Add this contract as a consumer of its own subscription.
        COORDINATOR.addConsumer(s_subscriptionId, consumers[0]);
    }

    // Assumes this contract owns link.
    // 1000000000000000000 = 1 LINK
    function topUpSubscription(uint256 amount) external onlyOwner {
        LINKTOKEN.transferAndCall(
            address(COORDINATOR),
            amount,
            abi.encode(s_subscriptionId)
        );
    }

    function addConsumer(address consumerAddress) external onlyOwner {
        // Add a consumer contract to the subscription.
        COORDINATOR.addConsumer(s_subscriptionId, consumerAddress);
    }

    function removeConsumer(address consumerAddress) external onlyOwner {
        // Remove a consumer contract from the subscription.
        COORDINATOR.removeConsumer(s_subscriptionId, consumerAddress);
    }

    function cancelSubscription(address receivingWallet) external onlyOwner {
        // Cancel the subscription and send the remaining LINK to a wallet address.
        COORDINATOR.cancelSubscription(s_subscriptionId, receivingWallet);
        s_subscriptionId = 0;
    }

    // Transfer this contract's funds to an address.
    // 1000000000000000000 = 1 LINK
    function withdraw(uint256 amount, address to) external onlyOwner {
        LINKTOKEN.transfer(to, amount);
    }

    // This is the callback function triggered by Chainlink VRF coordinator V2.
    // This function is triggered by Chainlink once COORDINATOR.requestRandomWord has been fullfilled
    function fulfillRandomWords(
        uint256 _requestId,
        uint256[] memory randomWords
    ) internal override {
        require(
            requestIdToTokenId[_requestId] > 0,
            "The RequestId received from Chainlink doesnt correlate to a Canary Advanced NFT Token Id"
        );
        s_randomWords = randomWords;
        uint256 tokenId = requestIdToTokenId[_requestId];

        uint256 randomBreed = (randomWords[0] % _numberBreed) + 1;
        tokenIdToCanaryRandomBreed[tokenId] = randomBreed;

        emit randomBreedAssigned(_requestId, randomBreed);
    }

    function setTokenUri(uint256 tokenId, string memory tokenUri)
        external
        onlyOwner
    {
        require(
            tokenIdToCanaryRandomBreed[tokenId] > 0,
            "The TokenId has no Random Breed assigned"
        );
        require(bytes(tokenUri).length > 0, "Token URI cannot be empty");
        _setTokenURI(tokenId, tokenUri);
        tokenIdToTokenURI[tokenId] = tokenUri;
        emit tokenMetadataGenerated(tokenId, tokenUri);
    }
}
