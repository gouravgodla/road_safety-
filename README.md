# road_safety-
Here's a draft README for your project:

---

# Road Safety Project

This project uses YOLOv8 to detect traffic violations and send email alerts. It monitors mixed-mode Foot Over Bridges (FOB) to ensure that pedestrians, bicycles, and motorcycles follow the rules.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/gouravgodla/road_safety-.git
   cd road_safety-
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the YOLOv8 model weights:
   ```bash
   # Download yolov8s.pt or another version
   ```

## Usage

1. Update the email configuration in `model.py` with your SMTP server details.
2. Run the script:
   ```bash
   python model.py
   ```

## Configuration

- **FOB_ENTRY**: Define the entry point coordinates for the FOB.
- **FOB_EXIT**: Define the exit point coordinates for the FOB.
- **Classes**: The script is pre-configured to detect pedestrians, bicycles, and motorcycles.

## Dependencies

- OpenCV
- NumPy
- ultralytics (for YOLOv8)
- smtplib (for sending emails)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

---

Feel free to update the details as per your project's requirements.
