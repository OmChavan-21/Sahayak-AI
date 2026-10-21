package com.sahayak.app.ui.screens

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import android.net.Uri
import android.graphics.BitmapFactory
import androidx.compose.foundation.Image
import androidx.compose.runtime.produceState
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.platform.LocalContext
import kotlinx.coroutines.withContext
import kotlinx.coroutines.Dispatchers

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

@Composable
fun AnalyzeScreen(
    initialText: String? = null,
    onAnalyze: (String) -> Unit,
    onAnalyzeImage: (String) -> Unit,
    onBack: () -> Unit,
    modifier: Modifier = Modifier
) {
    var textInput by rememberSaveable { mutableStateOf(initialText ?: "") }
    var selectedImageUri by rememberSaveable { mutableStateOf<String?>(null) }
    
    val photoPickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia()
    ) { uri: Uri? ->
        if (uri != null) {
            selectedImageUri = uri.toString()
        }
    }


    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = "Analyze Something",
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = "Paste a message, payment request, link, or other digital content.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        Spacer(modifier = Modifier.height(24.dp))

        if (initialText != null) {
            Text(
                text = "Imported from another app",
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(8.dp))
        }

        if (selectedImageUri != null) {
            Text(
                text = "Image selected",
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(8.dp))
            
            val context = LocalContext.current
            val bitmapState = produceState<android.graphics.Bitmap?>(initialValue = null, selectedImageUri) {
                value = withContext(Dispatchers.IO) {
                    try {
                        val uri = Uri.parse(selectedImageUri)
                        context.contentResolver.openInputStream(uri)?.use { 
                            BitmapFactory.decodeStream(it)
                        }
                    } catch (e: Exception) { null }
                }
            }
            
            bitmapState.value?.let { bitmap ->
                Image(
                    bitmap = bitmap.asImageBitmap(), 
                    contentDescription = "Selected Image Preview", 
                    modifier = Modifier.fillMaxWidth().weight(1f)
                )
            } ?: run {
                Spacer(modifier = Modifier.weight(1f))
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            Button(
                onClick = { onAnalyzeImage(selectedImageUri!!) },
                modifier = Modifier.fillMaxWidth().height(56.dp)
            ) {
                Text("Analyze Image", style = MaterialTheme.typography.titleMedium)
            }
            
            Spacer(modifier = Modifier.height(12.dp))
            
            OutlinedButton(
                onClick = { selectedImageUri = null },
                modifier = Modifier.fillMaxWidth().height(56.dp)
            ) {
                Text("Choose Another Image", style = MaterialTheme.typography.titleMedium)
            }
            
        } else {
            OutlinedTextField(
                value = textInput,
                onValueChange = { textInput = it },
                placeholder = { Text("Paste or type the message here...") },
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f),
                maxLines = 20
            )

            Spacer(modifier = Modifier.height(24.dp))

            OutlinedButton(
                onClick = { photoPickerLauncher.launch(androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)) },
                modifier = Modifier.fillMaxWidth().height(56.dp)
            ) {
                Text("Choose Image", style = MaterialTheme.typography.titleMedium)
            }
            
            Spacer(modifier = Modifier.height(12.dp))

            Button(
                onClick = { if (textInput.isNotBlank()) onAnalyze(textInput) },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                enabled = textInput.isNotBlank()
            ) {
                Text(
                    text = "Analyze",
                    style = MaterialTheme.typography.titleMedium
                )
            }
            
            Spacer(modifier = Modifier.height(12.dp))

            OutlinedButton(
                onClick = { textInput = "" },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp)
            ) {
                Text(
                    text = "Clear",
                    style = MaterialTheme.typography.titleMedium
                )
            }
        }    }
}
