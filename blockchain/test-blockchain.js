/**
 * TourShield - Local Blockchain Ledger & Digital ID Simulator
 * Demonstrates cryptographic pass issuance, DID verification, and immutable incident logging.
 */

const crypto = require('crypto');

class TourShieldBlockchain {
  constructor() {
    this.chain = [];
    this.touristPasses = {};
    this.incidentLedger = [];
    this.authorityAdmin = "0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7";

    // Genesis Block
    this.createBlock("GENESIS_BLOCK", "0");
  }

  // SHA-256 Cryptographic Hash
  calculateHash(data, previousHash, timestamp) {
    return crypto
      .createHash('sha256')
      .update(previousHash + timestamp + JSON.stringify(data))
      .digest('hex');
  }

  createBlock(data, previousHash) {
    const timestamp = Date.now();
    const hash = this.calculateHash(data, previousHash, timestamp);
    const block = {
      blockNumber: this.chain.length + 1,
      timestamp: new Date(timestamp).toLocaleTimeString(),
      data: data,
      previousHash: previousHash,
      hash: hash
    };
    this.chain.push(block);
    return block;
  }

  // 1. Issue Privacy-Preserving Tourist Digital ID (DID)
  issueTouristPass(passportOrAadhaarNumber, validDays, emergencyContact) {
    // Hash sensitive identity to maintain complete privacy
    const didHash = "DID:ETH:0x" + crypto.createHash('sha256').update(passportOrAadhaarNumber).digest('hex').substring(0, 16);
    const expiryTimestamp = Date.now() + validDays * 24 * 60 * 60 * 1000;

    this.touristPasses[didHash] = {
      didHash,
      validUntil: expiryTimestamp,
      emergencyContact,
      isActive: true
    };

    // Log Pass generation into Blockchain
    const block = this.createBlock({ event: "PASS_ISSUED", didHash, validDays }, this.getLatestBlockHash());
    return { didHash, block };
  }

  // 2. Offline Checkpoint Pass Verification
  verifyPass(didHash) {
    const pass = this.touristPasses[didHash];
    if (!pass) return { valid: false, reason: "ID Not Registered" };
    if (!pass.isActive) return { valid: false, reason: "Pass Revoked" };
    if (Date.now() > pass.validUntil) return { valid: false, reason: "Pass Expired" };

    return {
      valid: true,
      didHash: pass.didHash,
      emergencyContact: pass.emergencyContact,
      status: "VERIFIED_ACTIVE"
    };
  }

  // 3. Log Immutable Incident to Blockchain Ledger
  reportIncident(didHash, incidentType, lat, lng) {
    const incidentData = {
      incidentId: this.incidentLedger.length + 1,
      didHash,
      incidentType,
      latitude: lat,
      longitude: lng,
      timestamp: new Date().toISOString()
    };

    this.incidentLedger.push(incidentData);

    // Mine new immutable block on-chain
    const block = this.createBlock({ event: "INCIDENT_REPORTED", incident: incidentData }, this.getLatestBlockHash());
    return { incidentData, block };
  }

  getLatestBlockHash() {
    return this.chain[this.chain.length - 1].hash;
  }
}

// ==========================================
// Execution Demonstration
// ==========================================
console.log("=========================================================");
console.log("🔗 TourShield: Blockchain Ledger Initialized");
console.log("=========================================================");

const tourShieldChain = new TourShieldBlockchain();

// 1. Issue Digital ID
console.log("\n[1] Issuing Privacy-Preserving Tourist DID...");
const tourist = tourShieldChain.issueTouristPass("PASS_IND_98765432", 7, "+919876543210");
console.log(`✅ Generated DID Hash: ${tourist.didHash}`);
console.log(`📦 Mined into Block #${tourist.block.blockNumber} (Hash: ${tourist.block.hash.substring(0, 24)}...)`);

// 2. Offline Checkpoint Verification
console.log("\n[2] Verifying Digital ID at Forest Ranger Checkpoint (Offline)...");
const verifyResult = tourShieldChain.verifyPass(tourist.didHash);
console.log(`🔍 Verification Result:`, verifyResult);

// 3. Log Emergency Incident on Blockchain
console.log("\n[3] Logging SOS Incident onto Immutable Ledger...");
const incident = tourShieldChain.reportIncident(tourist.didHash, "GEO_FENCE_BREACH", "28.6185", "77.2145");
console.log(`🚨 Incident Logged:`, incident.incidentData);
console.log(`📦 Mined into Block #${incident.block.blockNumber} (Hash: ${incident.block.hash.substring(0, 24)}...)`);

console.log("\n=========================================================");
console.log(`🔗 Total Blocks on Blockchain: ${tourShieldChain.chain.length}`);
console.log("=========================================================");