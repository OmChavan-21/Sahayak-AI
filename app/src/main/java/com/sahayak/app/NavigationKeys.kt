package com.sahayak.app

import androidx.navigation3.runtime.NavKey
import kotlinx.serialization.Serializable

@Serializable data object Main : NavKey

@Serializable data class Analyze(val sharedText: String? = null) : NavKey

@Serializable data class Result(val textToAnalyze: String? = null, val imageUri: String? = null) : NavKey
