package com.sahayak.app.capabilities

class CapabilityProtocolRegistry {
    private val capabilities = mutableMapOf<SahayakCapability, CapabilityMetadata>()

    fun register(metadata: CapabilityMetadata) {
        if (capabilities.containsKey(metadata.id)) {
            throw IllegalArgumentException("Capability ${metadata.id} is already registered")
        }
        capabilities[metadata.id] = metadata
    }

    fun getMetadata(id: SahayakCapability): CapabilityMetadata? {
        return capabilities[id]
    }

    fun getAllRegistered(): List<CapabilityMetadata> {
        return capabilities.values.toList()
    }
}
