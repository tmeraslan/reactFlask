# Currency Converter App

## Architecture

This project is split into two applications:

- **Backend (Flask)** – exposes a simple REST API:
  - `GET /health` – health check.
  - `POST /convert` – converts between USD, EUR, GBP, JPY using hardcoded rates.
- **Frontend (React)** – simple UI that calls the `/convert` endpoint and displays the result.

The UI is served as a **separate static application** (not bundled into Flask), for the following reasons:

1. Clear separation of concerns between backend and frontend.
2. Easier to containerize and scale each part independently.
3. More realistic setup for modern web applications (microservices).

In a production environment, the React app can be built into static files and served by a CDN or nginx, while Flask runs behind an API gateway or reverse proxy.

## How to run

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py


//The UI is served directly from the Flask backend.
Reasons:
- Simpler architecture (single container).
- No reverse proxy needed.
- Easier local development.



//The UI is served as a separate static container using Nginx.
Reasons:
- Better separation of concerns.
- UI and API can scale independently.
- Production-grade static serving via Nginx.
