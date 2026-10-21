package com.sahayak.app.ai

import com.sahayak.app.security.RiskLevel
import kotlinx.coroutines.runBlocking
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class MockLocalAIModelRuntime(
    override var currentState: ModelLifecycleState = ModelLifecycleState.READY,
    private val simulatedResponse: RuntimeResponse = RuntimeResponse.Unavailable
) : LocalAIModelRuntime {
    
    override val configuration: ModelConfiguration? = null

    override suspend fun loadModel(config: ModelConfiguration): Boolean = true
    
    override suspend fun generate(prompt: PromptContext): RuntimeResponse {
        return simulatedResponse
    }
    
    override suspend fun release() {}
    override suspend fun cancel() {}
}

class RuntimeBackedSahayakAIEngineTest {

    @Test
    fun testRuntimeUnavailableStateReturnsUnavailable() = runBlocking {
        val runtime = MockLocalAIModelRuntime(currentState = ModelLifecycleState.UNAVAILABLE)
        val engine = RuntimeBackedSahayakAIEngine(runtime)
        
        val request = SahayakAIRequest(
            task = SahayakAITask.ASSESS_SECURITY,
            securityContext = SahayakAISecurityContext(RiskLevel.NO_STRONG_INDICATORS, emptyList()),
            observedEvidence = emptyList(),
            untrustedContent = "test"
        )
        val result = engine.analyze(request)
        
        assertEquals(SahayakAIResult.Unavailable, result)
    }

    @Test
    fun testRuntimeLoadingStateReturnsUnavailable() = runBlocking {
        val runtime = MockLocalAIModelRuntime(currentState = ModelLifecycleState.LOADING)
        val engine = RuntimeBackedSahayakAIEngine(runtime)
        
        val request = SahayakAIRequest(
            task = SahayakAITask.ASSESS_SECURITY,
            securityContext = SahayakAISecurityContext(RiskLevel.NO_STRONG_INDICATORS, emptyList()),
            observedEvidence = emptyList(),
            untrustedContent = "test"
        )
        val result = engine.analyze(request)
        
        assertEquals(SahayakAIResult.Unavailable, result)
    }

    @Test
    fun testRuntimeErrorIsRepresentedSafely() = runBlocking {
        val runtime = MockLocalAIModelRuntime(
            currentState = ModelLifecycleState.READY,
            simulatedResponse = RuntimeResponse.Error("Out of memory")
        )
        val engine = RuntimeBackedSahayakAIEngine(runtime)
        
        val request = SahayakAIRequest(
            task = SahayakAITask.ASSESS_SECURITY,
            securityContext = SahayakAISecurityContext(RiskLevel.NO_STRONG_INDICATORS, emptyList()),
            observedEvidence = emptyList(),
            untrustedContent = "test"
        )
        val result = engine.analyze(request)
        
        assertTrue(result is SahayakAIResult.Error)
        assertEquals("Out of memory", (result as SahayakAIResult.Error).errorMessage)
    }

    @Test
    fun testRuntimeCancellationIsRepresentedSafely() = runBlocking {
        val runtime = MockLocalAIModelRuntime(
            currentState = ModelLifecycleState.READY,
            simulatedResponse = RuntimeResponse.Cancelled
        )
        val engine = RuntimeBackedSahayakAIEngine(runtime)
        
        val request = SahayakAIRequest(
            task = SahayakAITask.ASSESS_SECURITY,
            securityContext = SahayakAISecurityContext(RiskLevel.NO_STRONG_INDICATORS, emptyList()),
            observedEvidence = emptyList(),
            untrustedContent = "test"
        )
        val result = engine.analyze(request)
        
        assertTrue(result is SahayakAIResult.Error)
        assertEquals("Inference was cancelled", (result as SahayakAIResult.Error).errorMessage)
    }
}
