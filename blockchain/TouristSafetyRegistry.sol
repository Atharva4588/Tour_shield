// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title TourShield - TouristSafetyRegistry
 * @dev Manages time-bound Decentralized Digital IDs (DID) and immutable incident logs.
 */
contract TouristSafetyRegistry {
    address public authorityAdmin;

    struct TouristPass {
        string didHash;           // Hashed ID (Privacy-preserving)
        uint256 validUntil;      // Expiration UNIX timestamp
        string emergencyContact; // Emergency contact reference
        bool isActive;
    }

    struct IncidentRecord {
        uint256 incidentId;
        string didHash;
        string incidentType;     // "GEO_BREACH", "MANUAL_PANIC", "FALL_DETECTED"
        string latitude;
        string longitude;
        uint256 timestamp;
        bool isResolved;
    }

    mapping(string => TouristPass) private registeredPasses;
    IncidentRecord[] public incidentLogs;

    event PassIssued(string indexed didHash, uint256 validUntil);
    event IncidentReported(uint256 indexed incidentId, string indexed didHash, string incidentType, uint256 timestamp);
    event IncidentResolved(uint256 indexed incidentId, uint256 resolvedAt);

    modifier onlyAuthority() {
        require(msg.sender == authorityAdmin, "Unauthorized: Authority only.");
        _;
    }

    constructor() {
        authorityAdmin = msg.sender;
    }

    // Issue a time-bound pass to a tourist
    function issueTouristPass(
        string memory _didHash,
        uint256 _durationInDays,
        string memory _emergencyContact
    ) external onlyAuthority {
        require(bytes(_didHash).length > 0, "Invalid DID");
        uint256 expiry = block.timestamp + (_durationInDays * 1 days);

        registeredPasses[_didHash] = TouristPass({
            didHash: _didHash,
            validUntil: expiry,
            emergencyContact: _emergencyContact,
            isActive: true
        });

        emit PassIssued(_didHash, expiry);
    }

    // Offline checkpoint verification
    function verifyPass(string memory _didHash) external view returns (bool isValid, uint256 remainingTime) {
        TouristPass memory pass = registeredPasses[_didHash];
        if (!pass.isActive || block.timestamp > pass.validUntil) {
            return (false, 0);
        }
        return (true, pass.validUntil - block.timestamp);
    }

    // Record an emergency incident immutably on-chain
    function reportIncident(
        string memory _didHash,
        string memory _incidentType,
        string memory _latitude,
        string memory _longitude
    ) external returns (uint256) {
        uint256 newIncidentId = incidentLogs.length;

        incidentLogs.push(IncidentRecord({
            incidentId: newIncidentId,
            didHash: _didHash,
            incidentType: _incidentType,
            latitude: _latitude,
            longitude: _longitude,
            timestamp: block.timestamp,
            isResolved: false
        }));

        emit IncidentReported(newIncidentId, _didHash, _incidentType, block.timestamp);
        return newIncidentId;
    }

    // Mark incident resolved by rescue team
    function resolveIncident(uint256 _incidentId) external onlyAuthority {
        require(_incidentId < incidentLogs.length, "Invalid Incident ID");
        incidentLogs[_incidentId].isResolved = true;
        emit IncidentResolved(_incidentId, block.timestamp);
    }

    // Get total recorded incidents
    function getTotalIncidents() external view returns (uint256) {
        return incidentLogs.length;
    }
}