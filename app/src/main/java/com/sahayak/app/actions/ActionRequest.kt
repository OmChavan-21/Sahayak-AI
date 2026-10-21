package com.sahayak.app.actions

import com.sahayak.app.input.Evidence

data class ActionRequest(
    val actionType: ActionType,
    val description: String,
    val reason: String,
    val relatedEvidence: List<Evidence> = emptyList()
)
