# Astrological Insight Generator

A full-stack application that generates personalized astrological insights based on user birth details. It uses a local LLM (Llama 3 via Ollama) to generate natural language horoscopes and supports multilingual output (English/Hindi) using a translation layer.

## Features

*   **Zodiac Calculation**: Automatically infers zodiac sign from birth date.
*   **AI Insights**: Uses a local LLM (Llama 3) to generate unique, daily horoscopes.
*   **Multilingual Support**: Generates content in English and translates to Hindi on demand.
*   **Simple UI**: Clean, responsive HTML/CSS frontend.

## Prerequisites

1.  **Python 3.9+** installed.
2.  **Ollama** installed and running (for the local LLM).
    *   Download from [ollama.com](https://ollama.com).
    *   Run the following command in your terminal to pull the model:
        ```bash
        ollama run llama3
        ```
    *   *Note: Keep Ollama running in the background.*

## Installation

1.  **Clone or Navigate to the project folder**:
    ```bash
    cd /path/to/astro_assgn
    ```

2.  **Create a Virtual Environment** (Optional but recommended):
    ```bash
    conda create -n astro
    conda activate astro
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Start the Backend Server**:
    ```bash
    python main.py
    ```
    You should see output indicating the server is running on `http://0.0.0.0:8000`.

2.  **Access the App**:
    Open your web browser and navigate to:
    [http://localhost:8000](http://localhost:8000)

## Usage

1.  Enter your Name, Birth Date, Time, and Place.
2.  Select your preferred language (English or Hindi).
3.  Click "Generate Insight".
4.  The system will calculate your Zodiac sign and display a personalized message.

## Project Structure

*   `main.py`: FastAPI backend entry point. Handles API routes and serves the frontend.
*   `logic.py`: Contains business logic for Zodiac calculation, LLM integration, and translation.
*   `index.html`: The frontend user interface.
*   `requirements.txt`: List of Python dependencies.
