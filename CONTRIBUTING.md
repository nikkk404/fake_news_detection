# Contributing to ThreatGuard 🛡️

Thank you for your interest in contributing to **ThreatGuard — Fake News Detection**! We welcome bug reports, prompt engineering optimizations, UI enhancements, and documentation improvements.

## Code of Conduct

All contributors and participants agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

1. **Fork the Repository**: Click the **Fork** button on `https://github.com/nikkk404/fake_news_detection`.
2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/<your-username>/fake_news_detection.git
   cd fake_news_detection
   ```
3. **Set Up Upstream Remote**:
   ```bash
   git remote add upstream https://github.com/nikkk404/fake_news_detection.git
   git fetch upstream
   ```
4. **Create a Topic Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
5. **Install Dependencies & Test Locally**:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
6. **Commit Your Changes**:
   ```bash
   git add .
   git commit -m "feat(ui): add character counter and reset button"
   ```
7. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Submit a Pull Request**:
   * Navigate to `https://github.com/nikkk404/fake_news_detection`.
   * Open a Pull Request comparing your feature branch against `main`.
   * Provide a clear title and description of your modifications.

## Contribution Guidelines
* **Code Quality**: Follow PEP 8 guidelines for Python code.
* **Frontend Usability**: Ensure responsive behavior and accessible color contrast.
* **Security**: Never commit actual API keys or `.env` files.
