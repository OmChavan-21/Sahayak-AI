package com.sahayak.app.capabilities

import com.sahayak.app.actions.ActionType

enum class SahayakCapability(val actionType: ActionType?) {
    READ_USER_INPUT(null),
    READ_SHARED_CONTENT(null),
    READ_SELECTED_IMAGE(null),
    READ_SELECTED_DOCUMENT(null),
    EXTRACT_TEXT(null),
    EXTRACT_EVIDENCE(null),
    ANALYZE_SECURITY(null),
    HIGHLIGHT_EVIDENCE(ActionType.HIGHLIGHT_EVIDENCE),
    EXPLAIN_CONTENT(ActionType.EXPLAIN),
    CREATE_DRAFT(ActionType.CREATE_DRAFT),
    CREATE_CHECKLIST(null),
    CREATE_REMINDER(ActionType.CREATE_REMINDER),
    SAVE_SECURITY_EVENT(null),
    GENERATE_REPORT_DRAFT(null),
    INSPECT_URL(ActionType.INSPECT_URL),
    
    // Future capabilities (not implemented)
    READ_NOTIFICATION(null),
    READ_BROWSER_CONTEXT(null),
    CAMERA_CAPTURE(null),
    MICROPHONE_INPUT(null),
    CONTACT_SELECTION(null),
    FILE_SELECTION(null),
    SEND_MESSAGE(ActionType.SEND_MESSAGE),
    SUBMIT_REPORT(ActionType.SUBMIT_COMPLAINT),
    MAKE_PAYMENT(ActionType.MAKE_PAYMENT),
    CHANGE_ACCOUNT_INFORMATION(ActionType.CHANGE_ACCOUNT_INFORMATION),
    EXECUTE_CODE(ActionType.UNKNOWN)
}
