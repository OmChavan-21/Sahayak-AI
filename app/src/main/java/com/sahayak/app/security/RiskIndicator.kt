package com.sahayak.app.security

data class RiskIndicator(
    val type: IndicatorType,
    val evidence: String,
    val description: String
)

enum class IndicatorType {
    URGENCY,
    PAYMENT_REQUEST,
    LINK_PRESENCE,
    CREDENTIAL_REQUEST,
    SUSPICIOUS_PRESSURE
}
