// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

import "../interfaces/RandomnessManagerInterface.sol";

contract AdvancedCanaryCollectible is ERC721, ERC721URIStorage {
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

    RandomnessManagerInterface public RANDOMNESS_INTERFACE;

    mapping(uint256 => CanaryBreed) tokenIdToCanaryRandomBreed; //Store the Breed identified for one tokenId @todo : might be redundant with tokenIdToCanaryRandomBreedNumber
    mapping(uint256 => uint256) tokenIdToCanaryRandomBreedNumber; // Store teh random mumber identified per tokenId
    mapping(uint256 => uint256) tokenIdToRequestID; //Store the random requestId for each tokenId

    event randomBreedNumberAssigned(
        uint256 indexed tokenId,
        uint256 randomBreedNumber
    );
    event randomBreedAssigned(
        uint256 indexed tokenId,
        CanaryBreed randomCanaryBreed
    );
    event randomRequest(uint256 indexed tokenId, uint256 randomRequestId);

    Counters.Counter public tokenCounter;

    string nftName = "Simple Canary NFT";
    string nftSymbol = "sCAN";
    uint256 _numberBreed = 10;

    address internal s_owner;

    constructor(address randomnessManagerAdress) ERC721(nftName, nftSymbol) {
        //The subscription manager has been created outside of this contract as it will manage random numbers for more than one contract.
        RANDOMNESS_INTERFACE = RandomnessManagerInterface(
            randomnessManagerAdress
        );
        s_owner = msg.sender;
    }

    /* 
    @Dev Descrition
    @Dev args : none
    #Dec Returns: tokenId that has just been minted.
    */
    function mintCollection() public onlyOwner returns (uint256) {
        tokenCounter.increment();
        _safeMint(msg.sender, tokenCounter.current());

        // a random number is requested to the VRF Randomness manager and stored against the token ID.
        uint256 requestID = RANDOMNESS_INTERFACE.requestRandomWords();

        // the process of getting a random number is asynchronously completed by chainlink. Once chainlink has completed the randomisation request for requestId,
        // Chainlinlink will then call back fulfillRandomWords() in the RandomnessManager contract. The random numnber will be stored in randomManager._s_randomWords[0]

        tokenIdToRequestID[tokenCounter.current()] = requestID;
        emit randomRequest(tokenCounter.current(), requestID);

        return tokenCounter.current(); // this need to be fixed as we ll need to genereate multiple tokens during collection creation
    }

    function revealTokenId(uint256 tokenId) public onlyOwner {
        require(
            tokenIdToRequestID[tokenId] > 0,
            "The tokenId your are trying to reveal hasn't requested a random number to chainlink RamdomManager"
        );
        require(
            RANDOMNESS_INTERFACE.getRandomWords() > 0,
            "The random number for the tokenID your are trying to reveal hasn't yet been provided by chainlink"
        );

        // We geenreate random breed for Canary NFTs
        uint256 randomCanaryBreedNumber = RANDOMNESS_INTERFACE
            .getRandomWords() % _numberBreed;
        tokenIdToCanaryRandomBreedNumber[tokenId] = randomCanaryBreedNumber;
        emit randomBreedNumberAssigned(tokenId, randomCanaryBreedNumber);

        CanaryBreed randomCanaryBreed = CanaryBreed(randomCanaryBreedNumber);
        tokenIdToCanaryRandomBreed[tokenId] = randomCanaryBreed;
        emit randomBreedAssigned(tokenId, randomCanaryBreed);

        //_setTokenURI(tokenId, tokenURI_);
    }

    function canaryRandomBreedByTokenID(uint256 tokenId)
        public
        view
        returns (uint256)
    {
        require(
            tokenIdToCanaryRandomBreedNumber[tokenId] > 0,
            "There is no random breed for the given Token Id"
        );
        return tokenIdToCanaryRandomBreedNumber[tokenId];
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
}
