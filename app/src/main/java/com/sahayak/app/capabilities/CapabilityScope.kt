package com.sahayak.app.capabilities

data class CapabilityScope(
    val requireHttps: Boolean = true,
    val isReadOnly: Boolean = true,
    val allowCredentials: Boolean = false,
    val allowCookies: Boolean = false,
    val allowPrivateNetwork: Boolean = false,
    val allowArbitraryCodeExecution: Boolean = false,
    val allowUnrestrictedDownloads: Boolean = false
) {
    companion object {
        val LEAST_PRIVILEGE_URL_INSPECTION = CapabilityScope(
            requireHttps = true,
            isReadOnly = true,
            allowCredentials = false,
            allowCookies = false,
            allowPrivateNetwork = false,
            allowArbitraryCodeExecution = false,
            allowUnrestrictedDownloads = false
        )
        val DEFAULT_SAFE_SCOPE = CapabilityScope()
    }
}
