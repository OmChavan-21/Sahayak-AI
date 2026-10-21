package com.sahayak.app.actions

class ActionPolicyEngine {
    
    fun evaluate(request: ActionRequest): ActionDecision {
        return evaluate(request.actionType)
    }

    fun evaluate(actionType: ActionType): ActionDecision {
        val risk = ActionPolicy.getRiskLevel(actionType)
        
        return when (risk) {
            ActionRisk.SAFE -> ActionDecision.ALLOWED
            ActionRisk.REQUIRES_CONFIRMATION -> ActionDecision.REQUIRES_CONFIRMATION
            ActionRisk.USER_MUST_EXECUTE -> ActionDecision.USER_MUST_EXECUTE
            ActionRisk.BLOCKED -> ActionDecision.BLOCKED
        }
    }
}
