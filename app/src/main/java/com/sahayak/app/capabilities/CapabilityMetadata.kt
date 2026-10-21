package com.sahayak.app.capabilities

import com.sahayak.app.actions.ActionRisk

data class CapabilityMetadata(
    val id: SahayakCapability,
    val riskLevel: ActionRisk,
    val purpose: String,
    val requiredPermission: String?,
    val dataAccessed: List<String>,
    val requiresUserConfirmation: Boolean,
    val isImplemented: Boolean,
    val isAllowedInPrototype: Boolean,
    val hasExternalSideEffect: Boolean,
    val isReversible: Boolean,
    val requiresAudit: Boolean
)
