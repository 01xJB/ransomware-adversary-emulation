<div align="center">

# Identity-Estimation

**Image-Based Age and Gender Estimation for Research and Educational Use**

![License](https://img.shields.io/github/license/01xJB/Identity-Estimation?color=blue&style=for-the-badge)
![Version](https://img.shields.io/github/v/tag/01xJB/Identity-Estimation?color=blue&style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge)

</div>

---

## Overview

`Identity-Estimation` is a Python-based computer vision project designed to estimate a person's **age and gender from an input image**.

The project was originally inspired by [smahesh29](https://github.com/smahesh29) and refined to provide a more streamlined implementation and more accurate estimation results.

The tool can be used for:

- Computer vision experimentation
- Age estimation research
- Identity and demographic estimation research
- Application prototyping
- Controlled age-verification experiments
- Educational machine-learning projects

> ## Responsible Use
>
> This project is intended for **research, education, experimentation, and authorized application development**.
>
> Age and gender estimation from images is inherently probabilistic and should not be treated as a definitive determination of a person's identity, age, or gender.
>
> Do not use this software to make high-impact decisions about individuals without appropriate safeguards, consent, and additional verification methods.

---

## Features

| | |
|---|---|
| 🎯 **Age Estimation** | Estimates an individual's age range from an input image. |
| 👤 **Gender Estimation** | Provides an estimated gender classification based on the trained model. |
| 📊 **CSV Records** | Optionally stores estimation results in CSV files for later analysis. |
| 🏷️ **Image Aliases** | Allows images to be associated with usernames, aliases, or other identifiers. |
| 🖼️ **Image-Based Input** | Accepts local image files for analysis. |
| ⚙️ **Model Configuration** | Allows model parameters and age ranges to be adjusted for experimentation. |

---

## How It Works

The project processes an input image and uses pre-trained computer-vision models to generate age and gender estimates.

A typical workflow looks like:

```text
Input Image
     |
     v
Face Detection
     |
     v
Feature Extraction
     |
     v
Age / Gender Models
     |
     +----------------+
     |                |
     v                v
Age Estimate     Gender Estimate
     |                |
     +-------+--------+
             |
             v
       Optional CSV Record
```

The resulting age estimate is represented as an age range rather than an exact age.

---

## Requirements

- Python 3.x
- Dependencies listed in [`requirements.txt`](requirements.txt)
- Pre-trained model files
- A supported image containing a detectable face

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/01xJB/Identity-Estimation.git
cd Identity-Estimation
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Pre-Trained Models

The pre-trained model files are distributed separately because of GitHub's individual file-size limitations.

Download the model archive from the following Mega.nz repository:

```text
https://mega.nz/file/6vYkzArR#IFVD61aWDJGJTswegk8xjr2_1OEwNBg21QK2eVEAFbk
```

Extract the contents of `models.zip` into the same directory as the Python program.

Your directory should resemble:

```text
Identity-Estimation/
├── main.py
├── requirements.txt
├── models/
│   └── ...
└── ...
```

---

## Usage

### Prepare an Image

Place a clear image containing the person you want to analyze in the project directory.

### Run the Program

```bash
python3 main.py
```

The program will prompt you for information such as whether the results should be saved and which CSV file should be used.

For example:

```text
Do you want to save results to a CSV file? (yes/no): yes
Enter the CSV file name: users
Enter an alias for the image (optional): myself
```

The resulting estimation may look similar to:

```text
Gender: Male
Age: 18-20 years
```

If the same CSV file is selected for multiple scans, additional results can be appended to the existing records.

---

## Windows Usage

### Create a Virtual Environment

```bash
python3 -m venv venv
```

Alternatively, specify the path to your Python installation:

```bash
C:\Users\USER\AppData\Local\Programs\PythonX\python.exe -m venv venv
```

### Activate the Virtual Environment

```powershell
.\venv\Scripts\activate
```

### Install Requirements

```bash
pip install -r requirements.txt
```

### Run the Program

```bash
python main.py --image image.jpg
```

For convenience, the image can be placed in the same directory as the Python program.

---

## Example

```bash
$ python3 main.py --image image.jpg

Do you want to save results to a CSV file? (yes/no): yes
Enter the CSV file name: users
Enter an alias for the image (optional): myself

Gender: Male
Age: 18-20 years
```

---

## Configuration

The project provides configurable model parameters that can be adjusted for experimentation and refinement.

### Confidence / Model Mean Values

The `self.model_mean_values` values can be modified to experiment with the model's age and gender estimation results.

```python
self.model_mean_values
```

Adjusting these values may affect the resulting predictions.

### Age Ranges

The `self.age_list` list controls the age ranges returned by the application.

```python
self.age_list
```

The ranges can be modified to create larger or smaller age intervals depending on the intended use case.

For example:

```text
18-20 years
21-25 years
26-30 years
```

---

## CSV Records

When CSV recording is enabled, results can be stored for later analysis.

A typical workflow is:

```text
Image
  |
  v
Age / Gender Estimation
  |
  v
Alias
  |
  v
CSV Record
```

This allows multiple images to be analyzed while keeping their results associated with a specified username or alias.

---

## Project Structure

```text
Identity-Estimation/
│
├── main.py
├── requirements.txt
├── models/
│   └── pre-trained models
│
└── ...
```

---

## Research and Learning Goals

This project can be used to gain practical experience with:

### Computer Vision

- Image processing
- Face detection
- Facial feature analysis
- Pre-trained machine-learning models
- Model inference

### Machine Learning

- Model-based classification
- Age estimation
- Gender classification
- Model parameter tuning
- Prediction refinement

### Python Development

- File handling
- CSV data storage
- Command-line execution
- Virtual environments
- Dependency management

---

## What This Project Is

This project is:

- A computer-vision research project
- An age-estimation experiment
- A gender-estimation experiment
- An educational machine-learning tool
- A Python development project
- A controlled image-analysis utility

## What This Project Is Not

This project should **not** be treated as a definitive identity-verification system.

It should not be used as the sole mechanism for:

- Determining a person's actual age
- Determining a person's identity
- Making high-impact decisions about individuals
- Replacing government-issued identification
- Replacing human verification
- Making sensitive decisions solely from model predictions

Model predictions can be inaccurate and should be treated as estimates.

---

## Disclaimer

This software is provided for **educational, research, and authorized testing purposes**.

Age and gender predictions generated by machine-learning models are estimates and may be incorrect due to image quality, lighting, facial characteristics, model limitations, or other factors.

Always consider privacy, consent, applicable laws, and organizational policies when processing images of individuals.

The author assumes no responsibility for decisions, damages, or consequences resulting from the use or misuse of this software.

---

## License

Released under the license included with this repository.

---

<div align="center">

Built by [**01xJB**](https://github.com/01xJB)

</div>
