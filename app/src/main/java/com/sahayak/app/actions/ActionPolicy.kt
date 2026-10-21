package com.sahayak.app.actions

object ActionPolicy {
    fun getRiskLevel(actionType: ActionType): ActionRisk {
        return when (actionType) {
            ActionType.EXPLAIN -> ActionRisk.SAFE
            ActionType.HIGHLIGHT_EVIDENCE -> ActionRisk.SAFE
            ActionType.CREATE_DRAFT -> ActionRisk.SAFE
            
            ActionType.CREATE_REMINDER -> ActionRisk.REQUIRES_CONFIRMATION
            ActionType.SHARE_INFORMATION -> ActionRisk.REQUIRES_CONFIRMATION
            
            ActionType.SEND_MESSAGE -> ActionRisk.USER_MUST_EXECUTE
            ActionType.SUBMIT_COMPLAINT -> ActionRisk.USER_MUST_EXECUTE
            
            ActionType.MAKE_PAYMENT -> ActionRisk.BLOCKED
            ActionType.CHANGE_ACCOUNT_INFORMATION -> ActionRisk.BLOCKED
            
            ActionType.INSPECT_URL -> ActionRisk.REQUIRES_CONFIRMATION
            ActionType.UNKNOWN -> ActionRisk.BLOCKED
        }
    }
}
