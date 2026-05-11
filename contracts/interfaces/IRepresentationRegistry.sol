// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title IRepresentationRegistry — AI Representation for Offline Nodes
/// @notice Manages which AI agents can vote on behalf of which nodes.
///         Every AI vote is tagged [REPRESENTED] and can be overridden within 24h.
/// @dev Implements C5.5 AI Temsil Sistemi

interface IRepresentationRegistry {
    // =========================================================================
    // EVENTS
    // =========================================================================

    event RepresentationEnabled(
        address indexed node,
        address indexed agent,
        uint256 offlineThreshold,
        uint256 timestamp
    );

    event RepresentationDisabled(
        address indexed node,
        uint256 timestamp
    );

    event RepresentationRulesUpdated(
        address indexed node,
        string rulesHash
    );

    // =========================================================================
    // STRUCTS
    // =========================================================================

    struct RepresentationConfig {
        address agent;              // AI agent's signing address
        bool enabled;
        uint256 offlineThreshold;   // seconds before AI activates (default: 86400 = 24h)
        uint256 graceperiod;        // seconds to override AI vote (default: 86400 = 24h)
        string rulesHash;           // hash of representation_rules from governance identity
        uint256 updatedAt;
    }

    // =========================================================================
    // CONFIGURATION
    // =========================================================================

    /// @notice Enable AI representation
    /// @param agent Address of the AI agent that will vote
    /// @param offlineThreshold Seconds offline before AI activates
    /// @param rulesHash Hash of the representation rules (off-chain verification)
    function enableRepresentation(
        address agent,
        uint256 offlineThreshold,
        string calldata rulesHash
    ) external;

    /// @notice Disable AI representation (immediate — all pending AI votes flagged)
    function disableRepresentation() external;

    /// @notice Update representation rules
    /// @param newRulesHash Hash of updated rules
    function updateRules(string calldata newRulesHash) external;

    /// @notice Update the agent address
    /// @param newAgent New AI agent signing address
    function updateAgent(address newAgent) external;

    // =========================================================================
    // QUERIES
    // =========================================================================

    /// @notice Check if a node has representation enabled
    function isRepresented(address node) external view returns (bool);

    /// @notice Check if a node is currently offline (past threshold)
    function isOffline(address node) external view returns (bool);

    /// @notice Get representation config for a node
    function getConfig(address node) external view returns (RepresentationConfig memory);

    /// @notice Check if an agent is authorized to represent a node
    function isAuthorizedAgent(address node, address agent) external view returns (bool);
}
