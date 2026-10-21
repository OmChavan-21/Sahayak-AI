package com.sahayak.app.audit

interface SecurityAuditSink {
    fun recordEvent(event: SecurityEvent)
    fun recordDecision(decision: SecurityDecisionRecord)
}

class InMemorySecurityAuditSink : SecurityAuditSink {
    private val events = mutableListOf<SecurityEvent>()
    private val decisions = mutableListOf<SecurityDecisionRecord>()
    
    override fun recordEvent(event: SecurityEvent) {
        // Enforce privacy constraint: don't store raw sensitive content
        require(event.sensitivityClassification != SensitivityClassification.SENSITIVE_CONTENT) {
            "Raw sensitive content cannot be audited."
        }
        events.add(event)
    }
    
    override fun recordDecision(decision: SecurityDecisionRecord) {
        decisions.add(decision)
    }

    fun getEvents(correlationId: String): List<SecurityEvent> {
        return events.filter { it.correlationId == correlationId }
    }
    
    fun getDecision(correlationId: String): SecurityDecisionRecord? {
        return decisions.find { it.correlationId == correlationId }
    }
    
    fun clear() {
        events.clear()
        decisions.clear()
    }
}
