package com.sahayak.app.actions

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
