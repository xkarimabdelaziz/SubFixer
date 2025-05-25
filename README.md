# SubFixer 🎬⏱️

A web-based tool built with Python and Flask for adjusting subtitle timings in `.srt` files. SubFixer helps you synchronize subtitles that are out of sync — whether they appear too early or too late — by allowing you to shift subtitle timings forward or backward with precision.

## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Notes](#notes)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Upload and Adjust**: Upload `.srt` files and shift subtitle timings as needed.
- **Increment/Decrement Support**: Easily add or subtract time to sync subtitles.
- **Instant Preview**: Adjust and download the updated file directly.
- **Web-Based Interface**: Simple, clean interface accessible via `http://127.0.0.1:5000`.
- **Built with Flask**: Lightweight and easy to run locally.

## Demo

![Screenshot 2025-05-26 010029](https://github.com/user-attachments/assets/bf2bfc2a-cb29-4e24-b591-cf7ca074c83c)


## Requirements
- **Python**: 3.x
- **Libraries**:
  - `flask`: For running the web server.
  - `pillow`: (If used for UI enhancement or file validation).

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/xkarimabdelaziz/SubFixer
   cd SubFixer
   ```

2. **Create a Virtual Environment** (optional but recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the Environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install flask pillow
   ```

5. **Run the App**
   ```bash
   python app.py
   ```

6. **Open in Browser**
   Visit `http://127.0.0.1:5000` in your browser.

## Usage

1. Upload your `.srt` subtitle file via the interface.
2. Enter the amount of time (in seconds) you want to shift.
3. Choose **Add** or **Subtract**.
4. Download the updated subtitle file.

## Project Structure

```
SubFixer/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # HTML frontend
├── static/             # Optional: for CSS/JS files
├── README.md           # Project documentation
└── requirements.txt    # (Optional) for pip installs
```

## Notes
- The app only supports `.srt` files at the moment.
- Time is adjusted for all subtitles uniformly.
- Built for local usage — no data is stored or shared externally.

## Contributing
Pull requests are welcome! To contribute:
1. Fork the repository.
2. Create a new branch.
3. Make your edits.
4. Submit a pull request.

## contact
instegram: xkarimabdelaziz 
twitter:   xkarimabdelaziz
