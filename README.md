# Watermark Tool

A simple GUI application for adding watermarks to images with customizable position, size, and opacity.

## Author
Sebastian Kowalec

## Features
- Add watermark to multiple images at once
- Preview watermark placement before processing
- Customize watermark:
  - Position (top-left, top-right, center, bottom-left, bottom-right)
  - Size (as percentage of image width)
  - Opacity (0-100%)
  - Offset from edges
- Support for multiple image formats (JPG, PNG, WEBP)
- Image queue management
- Live preview with navigation
- Maintains transparency for PNG and WEBP formats

## Installation

### Prerequisites
- Python 3.6 or higher
- PIL (Pillow) library

### Windows
1. Install Python from [python.org](https://python.org)
2. Open Command Prompt and run:
```bash
pip install Pillow# watermark

### macOS
1. Install Python using Homebrew:
```bash
brew install python
 ```

2. Install required package:
```bash
pip3 install Pillow
 ```

### Linux
1. Install Python and pip:
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
 ```
```

2. Install required package:
```bash
pip3 install Pillow
 ```

## Usage
1. Run the application:
```bash
python watermark.py
 ```

2. Select a watermark image
3. Add images to the queue
4. Choose output directory
5. Adjust watermark settings:
   - Size (percentage of image width)
   - Position
   - Opacity
   - Offset
6. Use the preview to check the result
7. Select output format (JPG, PNG, WEBP)
8. Click "Process Queue" to apply watermark to all images
## License
MIT License

## Contributing
Feel free to submit issues and pull requests