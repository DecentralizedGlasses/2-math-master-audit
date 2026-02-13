/*
* Verification of GasBadNftMarketplace
*/

using GasBadNftMarketplace as gasBadNftMarketplace;
using NftMarketplace as nftMarketplace;

methods {
     function getListing(address nftAddress, uint256 tokenId) external returns (INftMarketplace.Listing) envfree; 
     function getProceeds(address seller) external returns uint256 envfree;
    // Usually it will HAVOC if we didn't mentioned `_.` and do `HAVOC` calls but now will call only from known contracts
    // Use nftMock.safeTransferFrom for all safeTransferFrom calls
    function _.safeTransferFrom(address, address, uint256) external => DISPATCHER(true);
    function _.onERC721Received(address, address, uint256, bytes) external => DISPATCHER(true);
}

ghost mathint listingUpdatesCount {
    init_state axiom listingUpdatesCount == 0;
    // intitial vstate will be 0
    // require such to be true
}
ghost mathint log4Count {
    init_state axiom log4Count == 0;
}

hook Sstore s_listings[KEY address nftAddress][KEY uint256 tokenId].price uint256 price {
    listingUpdatesCount = listingUpdatesCount + 1;
}

hook LOG4(uint offset, uint length,  bytes32 t1, bytes32 t2, bytes32 t3, bytes32 t4) {
    log4Count = log4Count + 1;
}



// Rules

invariant anytime_mapping_updated_emit_event()
    listingUpdatesCount <= log4Count;


rule calling_any_function_should_result_in_each_contract_having_the_same_state(method f, method f2)
{
    require(f.selector == f2.selector);
    // 1. Going to call the same function on NftMarket and GasBad
    // 2. Compare the getter functions of both to conclude that they are same
    env e;
    calldataarg args;
    address listingAddress;
    uint256 tokenId;
    address seller;

    require(gasBadNftMarketplace.getProceeds(seller) == nftMarketplace.getProceeds(e, seller));
    require(gasBadNftMarketplace.getListing(listingAddress, tokenId).price == nftMarketplace.getListing(e,listingAddress, tokenId).price);
    require(gasBadNftMarketplace.getListing(listingAddress, tokenId).seller == nftMarketplace.getListing(e, listingAddress, tokenId).seller);

    // Act
    gasBadNftMarketplace.f(e, args);
    nftMarketplace.f2(e, args);

    // Assert
    assert(gasBadNftMarketplace.getProceeds(seller) == nftMarketplace.getProceeds(e, seller));
    assert(gasBadNftMarketplace.getListing(listingAddress, tokenId).price == nftMarketplace.getListing(e, listingAddress, tokenId).price);
    assert(gasBadNftMarketplace.getListing(listingAddress, tokenId).seller == nftMarketplace.getListing(e, listingAddress, tokenId).seller);

}