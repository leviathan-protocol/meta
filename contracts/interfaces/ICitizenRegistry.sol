// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title ICitizenRegistry — OpenPOS Citizen Registration
/// @notice Maps wallet addresses to POS hashes on-chain.
///         Proves a node HAS a POS without revealing its contents.
/// @dev Part of the OpenPOS Governance Bridge (Faz 3)

interface ICitizenRegistry {
    // =========================================================================
    // EVENTS
    // =========================================================================

    event CitizenRegistered(
        address indexed wallet,
        bytes32 posHash,
        string posVersion,
        uint8 visibility,
        uint256 timestamp
    );

    event POSUpdated(
        address indexed wallet,
        bytes32 oldHash,
        bytes32 newHash,
        string newVersion,
        uint256 timestamp
    );

    event VisibilityChanged(
        address indexed wallet,
        uint8 oldVisibility,
        uint8 newVisibility
    );

    event CitizenWithdrawn(
        address indexed wallet,
        uint256 timestamp
    );

    // =========================================================================
    // STRUCTS
    // =========================================================================

    struct Citizen {
        bytes32 posHash;        // SHA-256 of full local POS
        string posVersion;      // e.g., "v2.0"
        uint8 visibility;       // 0=ghost, 1=selective, 2=transparent
        uint256 registeredAt;
        uint256 lastActive;
        bool active;            // false = withdrawn (but never deleted — immutable rule #1)
    }

    // =========================================================================
    // REGISTRATION
    // =========================================================================

    /// @notice Register as a citizen with a POS hash
    /// @param posHash SHA-256 hash of the full local POS
    /// @param posVersion Current POS version string
    /// @param visibility 0=ghost, 1=selective, 2=transparent
    function register(
        bytes32 posHash,
        string calldata posVersion,
        uint8 visibility
    ) external;

    /// @notice Update POS hash when POS evolves
    /// @param newHash New SHA-256 hash after POS change
    /// @param newVersion New POS version string
    function updatePOS(
        bytes32 newHash,
        string calldata newVersion
    ) external;

    /// @notice Change visibility level
    /// @param newVisibility 0=ghost, 1=selective, 2=transparent
    function setVisibility(uint8 newVisibility) external;

    /// @notice Withdraw from governance (soft delete — node still exists per B2 rule #1)
    function withdraw() external;

    /// @notice Re-activate after withdrawal
    function reactivate(
        bytes32 posHash,
        string calldata posVersion
    ) external;

    // =========================================================================
    // QUERIES
    // =========================================================================

    /// @notice Check if an address is a registered citizen
    function isCitizen(address wallet) external view returns (bool);

    /// @notice Check if a citizen is active (not withdrawn)
    function isActive(address wallet) external view returns (bool);

    /// @notice Get citizen data
    function getCitizen(address wallet) external view returns (Citizen memory);

    /// @notice Get total registered citizens
    function totalCitizens() external view returns (uint256);

    /// @notice Get total active citizens
    function activeCitizens() external view returns (uint256);
}
