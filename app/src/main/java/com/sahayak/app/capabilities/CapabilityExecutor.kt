package com.sahayak.app.capabilities

/**
 * The strict boundary for executing capabilities. 
 * AI cannot directly call Android APIs. It must route through here.
 */
interface CapabilityExecutor {
    suspend fun execute(request: CapabilityRequest, decision: CapabilityDecision): Boolean
}
