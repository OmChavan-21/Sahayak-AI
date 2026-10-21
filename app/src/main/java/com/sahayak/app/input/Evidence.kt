package com.sahayak.app.input

/**
 * Evidence represents information extracted from an input.
 * It distinguishes between what was actually present (sourceSnippet) and what was extracted/interpreted (value).
 */
data class Evidence(
    val type: EvidenceType,
    val value: String, // Interpreted or normalized value
    val sourceSnippet: String // The exact text snippet observed in the input
)
