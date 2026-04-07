import os

# Check the cache directory for DialoGPT-medium
cache_dir = os.path.expanduser('~/.cache/huggingface/hub/models--microsoft--DialoGPT-medium')
print(f'Cache dir: {cache_dir}')
print(f'Cache dir exists: {os.path.exists(cache_dir)}')

if os.path.exists(cache_dir):
    # List all files in the cache directory
    files = os.listdir(cache_dir)
    print(f'Files in cache: {files}')
    
    # Look for pytorch_model.bin
    for f in files:
        if 'pytorch_model.bin' in f:
            path = os.path.join(cache_dir, f)
            size = os.path.getsize(path)
            size_mb = size / 1024 / 1024
            expected_size = 863  # MB
            percentage = (size_mb / expected_size) * 100
            print(f'{f}: {size_mb:.2f} MB ({percentage:.1f}%)')
            break
    else:
        print('pytorch_model.bin not found in cache')
else:
    print('Cache directory does not exist')
