# GPT-4 Image Analysis Script

This Python script utilizes the OpenAI GPT-4 API to analyze images, extract text, and categorize the content into Title, Body, and Footer. It is designed to process a given image, identify text regions, and categorize the text based on its position and context within the image.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have a `Windows/Linux/Mac` machine.
* You have installed the latest version of `Python`.
* You have an OpenAI API key.

## Installation

Clone the project repository to your local machine:

```bash
git clone https://github.com/Grant-Howard-32/SSDevOps.git
```

Navigate to the project directory:

```bash
cd SSDevOps
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

## Configuration

Create a .env file in the project root directory and add your OpenAI API key:

```
OPENAI_API_KEY='Your-OpenAI-API-Key-Here'
```

## Usage

Add images to the images directory.

Edit the following line in gptVision.py:

```python
image_path = "images/[name of your image].jpg"
```

Run the script using Python:

```bash
python image_analysis_script.py
```

## Contributing

Contributions to this project are welcome. To contribute:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/your_feature).
3. Make your changes.
4. Commit your changes (git commit -am 'Add some feature').
5. Push to the branch (git push origin feature/your_feature).
6. Create a new Pull Request.



