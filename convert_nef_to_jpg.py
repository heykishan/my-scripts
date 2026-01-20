from PIL import Image
import rawpy
import sys
from pathlib import Path

def convert_nef_to_jpg(input_path, output_path=None, quality=95):
    """Convert a single NEF file to JPG."""
    input_path = Path(input_path)
    
    if output_path is None:
        output_path = input_path.with_suffix('.jpg')
    
    with rawpy.imread(str(input_path)) as raw:
        rgb = raw.postprocess()
    
    image = Image.fromarray(rgb)
    image.save(output_path, 'JPEG', quality=quality)
    print(f"✓ {input_path.name} -> {output_path.name}")

def batch_convert(input_dir, output_dir=None, quality=95):
    """Convert all NEF files in a directory."""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir) if output_dir else input_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # More robust pattern matching for NEF files
    nef_files = list(input_dir.glob('*.[Nn][Ee][Ff]'))
    
    if not nef_files:
        print(f"No NEF files found in {input_dir}")
        print(f"Checking directory contents...")
        all_files = list(input_dir.iterdir())
        print(f"Total files: {len(all_files)}")
        for f in all_files[:5]:  # Show first 5 files
            print(f"  - {f.name}")
        return
    
    print(f"Found {len(nef_files)} NEF files. Converting...")
    
    success_count = 0
    fail_count = 0
    
    for nef_file in nef_files:
        output_path = output_dir / nef_file.with_suffix('.jpg').name
        try:
            convert_nef_to_jpg(nef_file, output_path, quality)
            success_count += 1
        except Exception as e:
            print(f"✗ Failed: {nef_file.name} - {e}")
            fail_count += 1
    
    print(f"\nDone! ✓ {success_count} converted, ✗ {fail_count} failed")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py <input_folder> [output_folder] [quality]")
        print("Example: python convert.py '/Users/kb/Documents/Trip pics'")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else None
    quality = int(sys.argv[3]) if len(sys.argv) > 3 else 95
    
    batch_convert(input_folder, output_folder, quality)
