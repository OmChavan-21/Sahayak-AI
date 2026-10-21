package com.sahayak.app.audit

import com.sahayak.app.input.InputType
import com.sahayak.app.actions.ActionDecision
import com.sahayak.app.capabilities.CapabilityRequest

data class SecurityDecisionRecord(
    val correlationId: String,
    val inputCategory: InputType,
    val evidenceReferences: List<String>,
    val aiRecommendationId: String?,
    val capabilityRequest: CapabilityRequest?,
    val policyDecision: ActionDecision,
    val userDecision: UserDecision,
    val finalOutcome: FinalOutcome,
    val reasonCode: SecurityReasonCode
)

enum class UserDecision {
    CONFIRMED,
    REJECTED,
    NOT_APPLICABLE,
    PENDING
}

enum class FinalOutcome {
    ALLOWED,
    BLOCKED,
    EXECUTED,
    UNAVAILABLE,
    PENDING
}
