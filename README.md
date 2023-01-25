# Auto-border-drawing
This python script draws a border around any object in the foreground of a selected rectangular region in the specified picture. The object in the foreground is detected using rembg library and uses openCV to edit the image as per the requirements.

## Requirements

```
python: >3.7, <3.11 requirement for rembg
rembg
OpenCV-Python
```

## Installation

Clone this repo.
```bash
git clone https://github.com/Jarosh-Antony/Auto-border-drawing
```

Create a virtual environment and activate it.
You can read about the creation and activation of virtual environment [here](https://docs.python.org/3/tutorial/venv.html).

```bash
pip install opencv-python
pip install rembg
```
OR
```bash
pip install -r requirement.txt
```

## Usage
The script can only run as a CLI.

- The flag `-i` is a must to specify the path of input image.
- The flag `-o` is optional. It specifies the output path and filename of the image while saving. Default saving path is same as input with filename appended with _output and uses same extension. While specifying the output filename, if the extension is not provided or OpenCV cannot save with specified extension, it uses the same extension of the input image.

### Windows
```bash
python main.py -i input.jpg
```

### Linux
```bash
python3 main.py -i input.jpg
```

### Follow the below procedure to draw the border:
- Use mouse to select a region by "click and drag"
- Press "ENTER" button to validate the region drawn by mouse
- Press "c" button to delete all borders and load original image
- Press "s" button to save the image with border. to the filename.
- Press "q" button to close or quit the script

