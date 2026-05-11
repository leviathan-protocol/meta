// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title IBranchManager — Governance Topic Branches
/// @notice Manages governance topic branches (domains) that nodes can subscribe to.
///         Proposals are filed under branches; nodes only see/vote on subscribed branches.

interface IBranchManager {
    // =========================================================================
    // EVENTS
    // =========================================================================

    event BranchCreated(
        string indexed branchId,
        address indexed creator,
        string name,
        uint256 timestamp
    );

    event BranchSubscribed(
        string indexed branchId,
        address indexed node
    );

    event BranchUnsubscribed(
        string indexed branchId,
        address indexed node
    );

    // =========================================================================
    // STRUCTS
    // =========================================================================

    struct Branch {
        string id;              // e.g., "ai-etik"
        string name;            // e.g., "AI Etik Kurallari"
        string description;
        address creator;
        uint256 subscriberCount;
        uint256 createdAt;
        bool active;
    }

    // =========================================================================
    // BRANCH MANAGEMENT
    // =========================================================================

    /// @notice Create a new governance branch
    function createBranch(
        string calldata id,
        string calldata name,
        string calldata description
    ) external;

    /// @notice Subscribe to a branch (receive proposals, can vote)
    function subscribe(string calldata branchId) external;

    /// @notice Unsubscribe from a branch
    function unsubscribe(string calldata branchId) external;

    // =========================================================================
    // QUERIES
    // =========================================================================

    /// @notice Get branch details
    function getBranch(string calldata branchId) external view returns (Branch memory);

    /// @notice Check if a node is subscribed to a branch
    function isSubscribed(string calldata branchId, address node) external view returns (bool);

    /// @notice Get all branches a node is subscribed to
    function getSubscriptions(address node) external view returns (string[] memory);

    /// @notice Get subscriber count for a branch
    function getSubscriberCount(string calldata branchId) external view returns (uint256);

    /// @notice List all active branches
    function listBranches() external view returns (string[] memory);
}
