// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AgriChain {
    struct ProduceBatch {
        uint256 batchId;
        string farmerId;
        string cropType;
        uint256 landAreaAcres;
        uint256 weightQuintals;
        string ipfsHash;
        uint256 timestamp;
        bool isVerified;
    }

    uint256 private _batchCounter;
    mapping(uint256 => ProduceBatch) public batches;

    event BatchRegistered(
        uint256 indexed batchId,
        string farmerId,
        string cropType,
        string ipfsHash,
        uint256 timestamp
    );

    function registerBatch(
        string memory _farmerId,
        string memory _cropType,
        uint256 _landAreaAcres,
        uint256 _weightQuintals,
        string memory _ipfsHash
    ) public returns (uint256) {
        _batchCounter++;
        uint256 newBatchId = _batchCounter;

        batches[newBatchId] = ProduceBatch({
            batchId: newBatchId,
            farmerId: _farmerId,
            cropType: _cropType,
            landAreaAcres: _landAreaAcres,
            weightQuintals: _weightQuintals,
            ipfsHash: _ipfsHash,
            timestamp: block.timestamp,
            isVerified: true
        });

        emit BatchRegistered(newBatchId, _farmerId, _cropType, _ipfsHash, block.timestamp);
        return newBatchId;
    }

    function getBatch(uint256 _batchId) public view returns (ProduceBatch memory) {
        require(_batchId > 0 && _batchId <= _batchCounter, "Batch does not exist.");
        return batches[_batchId];
    }
}