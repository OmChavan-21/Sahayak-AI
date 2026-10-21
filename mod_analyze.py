import io
path = 'app/src/main/java/com/sahayak/app/ui/screens/AnalyzeScreen.kt'
c = io.open(path, 'r', encoding='utf-8').read()

imports = """import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import android.net.Uri
import android.graphics.BitmapFactory
import androidx.compose.foundation.Image
import androidx.compose.runtime.produceState
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.platform.LocalContext
import kotlinx.coroutines.withContext
import kotlinx.coroutines.Dispatchers
"""
c = c.replace('import androidx.compose.foundation.layout.Column', imports + '\nimport androidx.compose.foundation.layout.Column')

c = c.replace('fun AnalyzeScreen(\n    initialText: String? = null,\n    onAnalyze: (String) -> Unit,', 
              'fun AnalyzeScreen(\n    initialText: String? = null,\n    onAnalyze: (String) -> Unit,\n    onAnalyzeImage: (String) -> Unit,')

inside_start = """    var textInput by rememberSaveable { mutableStateOf(initialText ?: "") }
    var selectedImageUri by rememberSaveable { mutableStateOf<String?>(null) }
    
    val photoPickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia()
    ) { uri: Uri? ->
        if (uri != null) {
            selectedImageUri = uri.toString()
        }
    }
"""
c = c.replace('    var textInput by rememberSaveable { mutableStateOf(initialText ?: "") }', inside_start)

# Change the textfield and buttons to switch between Image / Text modes
ui_replace = """        if (selectedImageUri != null) {
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
        }"""

start_idx = c.find('        OutlinedTextField(')
end_idx = c.find('    }\n}', start_idx)
c = c[:start_idx] + ui_replace + c[end_idx:]

io.open(path, 'w', encoding='utf-8').write(c)
