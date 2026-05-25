// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title X402ReceiptRegistry
/// @notice A minimal testnet contract for recording x402-style payment receipts.
/// @dev This contract does not transfer ETH, transfer ERC-20 tokens, request approvals, or custody funds.
contract X402ReceiptRegistry {
    struct Receipt {
        address payer;
        address token;
        uint256 amount;
        bytes32 endpointHash;
        uint256 timestamp;
    }

    string public serviceName;
    address public paymentRecipient;
    address public suggestedToken;
    uint256 public suggestedAmount;
    uint256 public paymentCount;

    mapping(bytes32 paymentId => Receipt receipt) private receipts;

    event PaymentRecorded(
        bytes32 indexed paymentId,
        address indexed payer,
        address indexed token,
        uint256 amount,
        bytes32 endpointHash
    );

    error PaymentAlreadyRecorded(bytes32 paymentId);
    error EmptyPaymentId();
    error EmptyEndpointHash();
    error ZeroAmount();
    error ZeroRecipient();

    constructor(
        string memory serviceName_,
        address paymentRecipient_,
        address suggestedToken_,
        uint256 suggestedAmount_
    ) {
        if (paymentRecipient_ == address(0)) revert ZeroRecipient();

        serviceName = serviceName_;
        paymentRecipient = paymentRecipient_;
        suggestedToken = suggestedToken_;
        suggestedAmount = suggestedAmount_;
    }

    function quote()
        external
        view
        returns (
            string memory name,
            address recipient,
            address token,
            uint256 amount
        )
    {
        return (serviceName, paymentRecipient, suggestedToken, suggestedAmount);
    }

    function recordPayment(
        bytes32 paymentId,
        bytes32 endpointHash,
        address token,
        uint256 amount
    ) external {
        if (paymentId == bytes32(0)) revert EmptyPaymentId();
        if (endpointHash == bytes32(0)) revert EmptyEndpointHash();
        if (amount == 0) revert ZeroAmount();
        if (receipts[paymentId].timestamp != 0) revert PaymentAlreadyRecorded(paymentId);

        receipts[paymentId] = Receipt({
            payer: msg.sender,
            token: token,
            amount: amount,
            endpointHash: endpointHash,
            timestamp: block.timestamp
        });
        paymentCount += 1;

        emit PaymentRecorded(paymentId, msg.sender, token, amount, endpointHash);
    }

    function getReceipt(bytes32 paymentId) external view returns (Receipt memory) {
        return receipts[paymentId];
    }
}
