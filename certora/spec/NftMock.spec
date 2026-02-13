/*
* Verification of NftMock
*/
using NftMock as nft;

methods {
    function totalSupply() external returns uint256 envfree;
    function mint() external;
    function balanceOf(address) external returns uint256 envfree;
}

// invariant totalSupplyIsNotNegative()
    // totalSupply() >= 0;


// rule minting_mints_one_nft() {
//     // Arrange
//     env e;
//     address minter;

//     require e.msg.value == 0;
//     require e.msg.sender == minter;
//     mathint balanceBefore = balanceOf(minter);

//     // Act
//     currentContract.mint(e);

//     // Assert
//     assert to_mathint(balanceOf(minter)) == balanceBefore +1, "Only 1 NFT should be minted";
// }
// rule sanity {
//     satisfy true;
// }

// rule no_change_to_total_supply(method f) {
//     uint256 totalSupplyBefore = totalSupply();

//     env e;
//     calldataarg arg;
//     f(e, arg);

//     assert totalSupply() == totalSupplyBefore, "Total supply should not change";
// }