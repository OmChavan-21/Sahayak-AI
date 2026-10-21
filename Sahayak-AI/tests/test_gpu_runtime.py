import unittest
import sys
import platform

class TestGpuRuntime(unittest.TestCase):
    def test_environment_isolation(self):
        # We must be running under Python 3.12, since 3.14 was CPU only
        self.assertEqual(sys.version_info.major, 3)
        self.assertEqual(sys.version_info.minor, 12)
        self.assertEqual(platform.system(), "Windows")
        
    def test_cuda_availability(self):
        import torch
        self.assertTrue(torch.cuda.is_available(), "CUDA must be available in the GPU environment.")
        self.assertGreater(torch.cuda.device_count(), 0)
        
    def test_no_cloud_enforcement(self):
        try:
            import openai
            self.fail("OpenAI SDK should not be installed in the GPU environment!")
        except ImportError:
            pass
            
        try:
            import google.generativeai
            self.fail("Google GenAI SDK should not be installed in the GPU environment!")
        except ImportError:
            pass

if __name__ == "__main__":
    unittest.main()
