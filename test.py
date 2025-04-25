import torch
print("✅ CUDA available:", torch.cuda.is_available())
print("🔧 CUDA version (from PyTorch):", torch.version.cuda)
print("📦 Torch version:", torch.__version__)
