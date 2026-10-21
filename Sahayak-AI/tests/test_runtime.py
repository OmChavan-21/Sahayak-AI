import unittest
import sys
import platform

class TestRuntime(unittest.TestCase):
    def test_environment_detection(self):
        self.assertGreaterEqual(sys.version_info[:2], (3, 8))
        self.assertEqual(platform.system(), "Windows")
        
    def test_no_cloud_enforcement(self):
        # We enforce no-cloud by checking that we don't have openai/google-genai dependencies
        try:
            import openai
            self.fail("OpenAI SDK should not be installed!")
        except ImportError:
            pass
            
        try:
            import google.generativeai
            self.fail("Google GenAI SDK should not be installed!")
        except ImportError:
            pass

    def test_dependencies(self):
        import torch
        import transformers
        import accelerate
        self.assertIsNotNone(torch.__version__)
        self.assertIsNotNone(transformers.__version__)
        self.assertIsNotNone(accelerate.__version__)
        
    def test_cuda_detection(self):
        import torch
        # Even if not available, the detection call itself should not crash
        has_cuda = torch.cuda.is_available()
        self.assertIsInstance(has_cuda, bool)

if __name__ == "__main__":
    unittest.main()
