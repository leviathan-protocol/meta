// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title IGovernanceVoting — OpenPOS Quadratic Voting
/// @notice Implements quadratic voting for Leviathan governance.
///         Vote power = sqrt(tokens) to prevent plutocracy.
/// @dev Threshold levels from B2 §Master Oylama Esik Tablosu:
///      Rutin=%60, Onemli=%66, Anayasal=%75, Misyon=%90+quorum, Degismez=%95+%75quorum

interface IGovernanceVoting {
    // =========================================================================
    // EVENTS
    // =========================================================================

    event VoteCast(
        uint256 indexed proposalId,
        address indexed voter,
        uint8 choice,          // 0=against, 1=for, 2=abstain
        uint256 weight,
        bool represented,      // true if AI voted on behalf
        string reasoning
    );

    event VoteOverridden(
        uint256 indexed proposalId,
        address indexed voter,
        uint8 oldChoice,
        uint8 newChoice
    );

    // =========================================================================
    // ENUMS
    // =========================================================================

    enum VoteChoice { Against, For, Abstain }

    enum ThresholdLevel {
        Routine,        // %60 — 24h tartisma
        Important,      // %66 — 48h tartisma
        Constitutional, // %75 — 72h tartisma
        Mission,        // %90 + %50 quorum — 90 gun tartisma
        Immutable       // %95 + %75 quorum — fork required
    }

    // =========================================================================
    // VOTING
    // =========================================================================

    /// @notice Cast a personal vote on a proposal
    /// @param proposalId The proposal to vote on
    /// @param choice Against(0), For(1), or Abstain(2)
    /// @param reasoning Human-readable reason for the vote
    function vote(
        uint256 proposalId,
        VoteChoice choice,
        string calldata reasoning
    ) external;

    /// @notice Cast a represented vote (AI voting on behalf of offline node)
    /// @dev Must be called by the node's registered representation agent
    /// @param proposalId The proposal to vote on
    /// @param voter The node being represented
    /// @param choice Against(0), For(1), or Abstain(2)
    /// @param reasoning AI's reasoning based on public_stances
    function representedVote(
        uint256 proposalId,
        address voter,
        VoteChoice choice,
        string calldata reasoning
    ) external;

    /// @notice Override an AI-cast vote within the grace period (24h)
    /// @param proposalId The proposal whose vote to override
    /// @param newChoice The corrected vote
    /// @param reasoning Reason for override
    function overrideVote(
        uint256 proposalId,
        VoteChoice newChoice,
        string calldata reasoning
    ) external;

    // =========================================================================
    // QUERIES
    // =========================================================================

    /// @notice Get vote count for a proposal (quadratic-weighted)
    /// @return forVotes Against votes, for votes, abstain count
    function getVoteCounts(uint256 proposalId)
        external view returns (uint256 forVotes, uint256 againstVotes, uint256 abstainCount);

    /// @notice Check if a proposal has reached its threshold
    function hasReachedThreshold(uint256 proposalId) external view returns (bool);

    /// @notice Check if override window is still open for a represented vote
    function canOverride(uint256 proposalId, address voter) external view returns (bool);

    /// @notice Calculate quadratic vote weight for an address
    /// @dev weight = sqrt(base_value + earned_xp + delegated_tokens)
    function getVoteWeight(address voter) external view returns (uint256);
}
