// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./IGovernanceVoting.sol";

/// @title IProposalSystem — OpenPOS Thesis/Antithesis/Synthesis
/// @notice Proposals follow dialectical structure: thesis → antithesis → synthesis.
///         Not just yes/no — genuine discourse before decision.
/// @dev Discourse protocol from B6-leviathan.md

interface IProposalSystem {
    // =========================================================================
    // EVENTS
    // =========================================================================

    event ProposalCreated(
        uint256 indexed id,
        address indexed proposer,
        string branch,
        IGovernanceVoting.ThresholdLevel level,
        uint256 discussionEnds,
        uint256 votingEnds
    );

    event AntithesisSubmitted(
        uint256 indexed proposalId,
        uint256 indexed antithesisId,
        address indexed submitter
    );

    event SynthesisProposed(
        uint256 indexed proposalId,
        uint256 indexed synthesisId,
        address indexed proposer
    );

    event ProposalFinalized(
        uint256 indexed id,
        ProposalOutcome outcome
    );

    // =========================================================================
    // ENUMS & STRUCTS
    // =========================================================================

    enum ProposalState {
        Discussion,     // thesis + antithesis phase
        Voting,         // voting phase
        Passed,
        Rejected,
        Synthesized,    // merged with antithesis into new proposal
        Expired
    }

    enum ProposalOutcome { Passed, Rejected, Synthesized, Expired }

    struct Proposal {
        uint256 id;
        address proposer;
        string branch;                          // governance topic branch
        IGovernanceVoting.ThresholdLevel level;  // determines threshold + discussion time

        string title;
        string thesis;                          // the proposal text
        string context;                         // why this matters

        uint256 createdAt;
        uint256 discussionEnds;                 // no voting before this
        uint256 votingEnds;

        ProposalState state;
    }

    struct Antithesis {
        uint256 id;
        uint256 proposalId;
        address submitter;
        string argument;
        uint256 createdAt;
    }

    struct Synthesis {
        uint256 id;
        uint256 proposalId;
        address proposer;
        string mergedProposal;                  // the combined proposal
        string reasoning;                       // how thesis + antithesis were reconciled
        uint256 createdAt;
    }

    // =========================================================================
    // PROPOSAL LIFECYCLE
    // =========================================================================

    /// @notice Create a new proposal
    /// @param branch Governance topic branch
    /// @param level Threshold level (determines discussion time and pass threshold)
    /// @param title Short title
    /// @param thesis The proposal text
    /// @param context Why this matters
    /// @return proposalId The new proposal's ID
    function createProposal(
        string calldata branch,
        IGovernanceVoting.ThresholdLevel level,
        string calldata title,
        string calldata thesis,
        string calldata context
    ) external returns (uint256 proposalId);

    /// @notice Submit an antithesis (counter-argument) during discussion phase
    /// @param proposalId The proposal to counter
    /// @param argument The counter-argument
    function submitAntithesis(
        uint256 proposalId,
        string calldata argument
    ) external returns (uint256 antithesisId);

    /// @notice Propose a synthesis (merged resolution) during discussion phase
    /// @param proposalId The original proposal
    /// @param mergedProposal The synthesized text
    /// @param reasoning How thesis and antithesis were reconciled
    function proposeSynthesis(
        uint256 proposalId,
        string calldata mergedProposal,
        string calldata reasoning
    ) external returns (uint256 synthesisId);

    /// @notice Finalize a proposal after voting ends
    /// @param proposalId The proposal to finalize
    function finalize(uint256 proposalId) external;

    // =========================================================================
    // QUERIES
    // =========================================================================

    /// @notice Get proposal details
    function getProposal(uint256 proposalId) external view returns (Proposal memory);

    /// @notice Get all antitheses for a proposal
    function getAntitheses(uint256 proposalId) external view returns (Antithesis[] memory);

    /// @notice Get all syntheses for a proposal
    function getSyntheses(uint256 proposalId) external view returns (Synthesis[] memory);

    /// @notice Get current state of a proposal
    function getState(uint256 proposalId) external view returns (ProposalState);

    /// @notice Get proposals in a branch
    function getProposalsByBranch(string calldata branch) external view returns (uint256[] memory);

    /// @notice Get active proposal count
    function activeProposalCount() external view returns (uint256);
}
