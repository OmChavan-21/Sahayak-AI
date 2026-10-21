package com.sahayak.app.input

interface EvidenceExtractor {
    fun extract(input: UserInput): List<Evidence>
}

class TextEvidenceExtractor : EvidenceExtractor {
    override fun extract(input: UserInput): List<Evidence> {
        val text = input.rawText ?: return emptyList()
        val evidenceList = mutableListOf<Evidence>()

        val urlRegex = "(https?://\\S+|www\\.\\S+)".toRegex()
        urlRegex.findAll(text).forEach { match ->
            evidenceList.add(
                Evidence(
                    type = EvidenceType.URL,
                    value = match.value,
                    sourceSnippet = match.value
                )
            )
        }

        val amountRegex = "(₹\\s*\\d+|\\$\\s*\\d+|Rs\\.?\\s*\\d+|\\d+\\s*(INR|USD))".toRegex(RegexOption.IGNORE_CASE)
        amountRegex.findAll(text).forEach { match ->
            evidenceList.add(
                Evidence(
                    type = EvidenceType.AMOUNT,
                    value = match.value,
                    sourceSnippet = match.value
                )
            )
        }

        val phoneRegex = "(\\+\\d{1,3}[- ]?\\d{9,10}|\\b\\d{10}\\b)".toRegex()
        phoneRegex.findAll(text).forEach { match ->
            evidenceList.add(
                Evidence(
                    type = EvidenceType.PHONE_NUMBER,
                    value = match.value,
                    sourceSnippet = match.value
                )
            )
        }

        val dateRegex = "(\\b\\d{1,2}[/-]\\d{1,2}[/-]\\d{2,4}\\b|\\b\\d{1,2}\\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\\b)".toRegex(RegexOption.IGNORE_CASE)
        dateRegex.findAll(text).forEach { match ->
            evidenceList.add(
                Evidence(
                    type = EvidenceType.DATE,
                    value = match.value,
                    sourceSnippet = match.value
                )
            )
        }

        return evidenceList
    }
}
