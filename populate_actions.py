import io

files = {}

files['app/src/main/java/com/sahayak/app/actions/ActionType.kt'] = """package com.sahayak.app.actions

enum class ActionType {
    EXPLAIN,
    HIGHLIGHT_EVIDENCE,
    CREATE_DRAFT,
    CREATE_REMINDER,
    SHARE_INFORMATION,
    SEND_MESSAGE,
    SUBMIT_COMPLAINT,
    MAKE_PAYMENT,
    CHANGE_ACCOUNT_INFORMATION,
    UNKNOWN
}
"""

files['app/src/main/java/com/sahayak/app/actions/ActionRisk.kt'] = """package com.sahayak.app.actions

enum class ActionRisk {
    SAFE,
    REQUIRES_CONFIRMATION,
    USER_MUST_EXECUTE,
    BLOCKED
}
"""

files['app/src/main/java/com/sahayak/app/actions/ActionDecision.kt'] = """package com.sahayak.app.actions

enum class ActionDecision {
    ALLOWED,
    REQUIRES_CONFIRMATION,
    USER_MUST_EXECUTE,
    BLOCKED
}
"""

files['app/src/main/java/com/sahayak/app/actions/ActionPolicy.kt'] = """package com.sahayak.app.actions

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
            
            ActionType.UNKNOWN -> ActionRisk.BLOCKED
        }
    }
}
"""

files['app/src/main/java/com/sahayak/app/actions/ActionRequest.kt'] = """package com.sahayak.app.actions

import com.sahayak.app.input.Evidence

data class ActionRequest(
    val actionType: ActionType,
    val description: String,
    val reason: String,
    val relatedEvidence: List<Evidence> = emptyList()
)
"""

files['app/src/main/java/com/sahayak/app/actions/ActionPolicyEngine.kt'] = """package com.sahayak.app.actions

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
"""

files['app/src/test/java/com/sahayak/app/actions/ActionPolicyEngineTest.kt'] = """package com.sahayak.app.actions

import org.junit.Assert.assertEquals
import org.junit.Test

class ActionPolicyEngineTest {

    private val engine = ActionPolicyEngine()

    @Test
    fun testExplainIsSafe() {
        assertEquals(ActionDecision.ALLOWED, engine.evaluate(ActionType.EXPLAIN))
    }

    @Test
    fun testHighlightEvidenceIsSafe() {
        assertEquals(ActionDecision.ALLOWED, engine.evaluate(ActionType.HIGHLIGHT_EVIDENCE))
    }

    @Test
    fun testCreateDraftIsSafe() {
        assertEquals(ActionDecision.ALLOWED, engine.evaluate(ActionType.CREATE_DRAFT))
    }

    @Test
    fun testCreateReminderRequiresConfirmation() {
        assertEquals(ActionDecision.REQUIRES_CONFIRMATION, engine.evaluate(ActionType.CREATE_REMINDER))
    }

    @Test
    fun testShareInformationRequiresConfirmation() {
        assertEquals(ActionDecision.REQUIRES_CONFIRMATION, engine.evaluate(ActionType.SHARE_INFORMATION))
    }

    @Test
    fun testSendMessageUserMustExecute() {
        assertEquals(ActionDecision.USER_MUST_EXECUTE, engine.evaluate(ActionType.SEND_MESSAGE))
    }

    @Test
    fun testSubmitComplaintUserMustExecute() {
        assertEquals(ActionDecision.USER_MUST_EXECUTE, engine.evaluate(ActionType.SUBMIT_COMPLAINT))
    }

    @Test
    fun testMakePaymentIsBlocked() {
        assertEquals(ActionDecision.BLOCKED, engine.evaluate(ActionType.MAKE_PAYMENT))
    }

    @Test
    fun testChangeAccountInformationIsBlocked() {
        assertEquals(ActionDecision.BLOCKED, engine.evaluate(ActionType.CHANGE_ACCOUNT_INFORMATION))
    }

    @Test
    fun testUnknownActionIsBlockedSafely() {
        assertEquals(ActionDecision.BLOCKED, engine.evaluate(ActionType.UNKNOWN))
    }
}
"""

for path, content in files.items():
    io.open(path, 'w', encoding='utf-8').write(content)
