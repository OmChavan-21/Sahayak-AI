package com.sahayak.app.security

class SecurityAnalyzer {

    fun analyze(text: String): SecurityAnalysis {
        val lowerText = text.lowercase()
        val indicators = mutableListOf<RiskIndicator>()

        val urgencyRegex = "(immediately|urgent|act now|within 24 hours|last warning|account will be blocked)".toRegex()
        urgencyRegex.find(lowerText)?.let {
            indicators.add(
                RiskIndicator(
                    type = IndicatorType.URGENCY,
                    evidence = it.value,
                    description = "Urgency detected"
                )
            )
        }

        val paymentRegex = "(pay|payment|₹|inr|transfer|send money|fee)".toRegex()
        paymentRegex.find(lowerText)?.let {
            val start = maxOf(0, it.range.first - 15)
            val end = minOf(text.length, it.range.last + 15)
            val evidenceSnippet = text.substring(start, end).trim()
            indicators.add(
                RiskIndicator(
                    type = IndicatorType.PAYMENT_REQUEST,
                    evidence = evidenceSnippet,
                    description = "Payment request detected"
                )
            )
        }

        val linkRegex = "(https?://\\S+|www\\.\\S+)".toRegex()
        linkRegex.find(lowerText)?.let {
            indicators.add(
                RiskIndicator(
                    type = IndicatorType.LINK_PRESENCE,
                    evidence = it.value,
                    description = "Link detected"
                )
            )
        }

        val credentialRegex = "(otp|pin|password|verification code|cvv)".toRegex()
        credentialRegex.find(lowerText)?.let {
            indicators.add(
                RiskIndicator(
                    type = IndicatorType.CREDENTIAL_REQUEST,
                    evidence = it.value,
                    description = "Credential or security code requested"
                )
            )
        }

        val pressureRegex = "(click now|don't ignore|verify immediately|your account will be suspended)".toRegex()
        pressureRegex.find(lowerText)?.let {
            indicators.add(
                RiskIndicator(
                    type = IndicatorType.SUSPICIOUS_PRESSURE,
                    evidence = it.value,
                    description = "Suspicious pressure language"
                )
            )
        }

        val riskLevel = determineRiskLevel(indicators)

        return SecurityAnalysis(
            riskLevel = riskLevel,
            indicators = indicators,
            explanation = getExplanation(riskLevel),
            recommendation = getRecommendation(riskLevel)
        )
    }

    private fun determineRiskLevel(indicators: List<RiskIndicator>): RiskLevel {
        if (indicators.isEmpty()) return RiskLevel.NO_STRONG_INDICATORS

        val hasPayment = indicators.any { it.type == IndicatorType.PAYMENT_REQUEST }
        val hasUrgency = indicators.any { it.type == IndicatorType.URGENCY }
        val hasLink = indicators.any { it.type == IndicatorType.LINK_PRESENCE }
        val hasCredential = indicators.any { it.type == IndicatorType.CREDENTIAL_REQUEST }
        val hasPressure = indicators.any { it.type == IndicatorType.SUSPICIOUS_PRESSURE }

        val highRiskCombos = (hasPayment && hasUrgency) ||
                (hasPayment && hasLink) ||
                (hasCredential && hasUrgency) ||
                (hasCredential && hasLink) ||
                (hasPressure && hasLink) ||
                (hasCredential)

        if (highRiskCombos || indicators.size >= 3) {
            return RiskLevel.HIGH_RISK
        } 
        
        val onlyPaymentOrLink = !hasUrgency && !hasCredential && !hasPressure
        if (onlyPaymentOrLink) {
            return RiskLevel.NO_STRONG_INDICATORS
        }

        return RiskLevel.AMBIGUOUS
    }

    private fun getExplanation(riskLevel: RiskLevel): String {
        return when (riskLevel) {
            RiskLevel.HIGH_RISK -> "Why this was flagged"
            RiskLevel.AMBIGUOUS -> "We found some warning signs, but there isn't enough evidence to determine whether this is fraudulent."
            RiskLevel.NO_STRONG_INDICATORS -> "We did not find strong warning indicators in the text provided. This does not guarantee that the message is legitimate."
            RiskLevel.UNABLE_TO_ANALYZE -> "Unable to read text from this image."
        }
    }

    private fun getRecommendation(riskLevel: RiskLevel): String {
        return when (riskLevel) {
            RiskLevel.HIGH_RISK -> "Don't click the link or make the payment. Verify the request through the organization's official app or website."
            RiskLevel.AMBIGUOUS -> "Do not take a risky action yet. Verify the request through an official source."
            RiskLevel.NO_STRONG_INDICATORS -> "Always remain cautious with unexpected messages."
            RiskLevel.UNABLE_TO_ANALYZE -> "Try a clearer image or provide the text another way."
        }
    }
}

