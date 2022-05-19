// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract SimpleCanaryCollectible is ERC721, ERC721URIStorage {
    using Counters for Counters.Counter;

    Counters.Counter public _nextTokenId;

    constructor() public ERC721("Simple Canary NFT", "sCAN") {}

    function createCollectible(string memory tokenURI_)
        public
        returns (uint256)
    {
        _nextTokenId.increment();
        uint256 currentTokenId = _nextTokenId.current();
        _safeMint(msg.sender, currentTokenId);
        _setTokenURI(currentTokenId, tokenURI_);
        return currentTokenId;
    }

    function totalSupply() public view returns (uint256) {
        return _nextTokenId.current();
    }

    // function _baseURI() internal pure override returns (string memory) {
    //     return
    //         "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json";
    // }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function _burn(uint256 tokenId)
        internal
        override(ERC721, ERC721URIStorage)
    {
        super._burn(tokenId);
    }
}
