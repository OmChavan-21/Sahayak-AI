package com.sahayak.app.capabilities

enum class TrustLevel(val level: Int) {
    LEVEL_0_UNTRUSTED_EXTERNAL(0),
    LEVEL_1_USER_PROVIDED_EVIDENCE(1),
    LEVEL_2_SYSTEM_VERIFIED(2),
    LEVEL_3_SAHAYAK_GENERATED(3),
    LEVEL_4_EXPLICIT_USER_CONFIRMED(4)
}
