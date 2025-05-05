# Internet Speed Logger 🚀

A web-based tool to log your internet speed (download/upload speeds and ping) over time and visualize the data through a graphical representation. The tool runs periodic speed tests and stores the results in a CSV file, which can be downloaded or visualized on a dashboard.

## Features:
- **Real-time Speed Logging**: Starts a test, logs results every 15 seconds for 2 minutes.
- **Data Visualization**: Displays internet speed trends with charts using Chart.js.
- **Downloadable Results**: Download the recorded speed data as a CSV file.
- **Rate Limiting**: Ensures the app isn't overloaded with requests.
- **Deployment**: Deployed using Render, accessible on the web.

## Getting Started

### Prerequisites
1. Python 3.x
2. Docker (for local development)
3. Redis (for rate limiting)
4. Gunicorn (for production)

### Installation

#### Local Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/internet-speed-logger.git
    cd internet-speed-logger
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run Redis locally if needed:
    ```bash
    docker run --name redis -p 6379:6379 -d redis
    ```

5. Run the app locally:
    ```bash
    flask run
    ```

   Or use **Gunicorn** for production setup:
    ```bash
    gunicorn -w 4 app:app
    ```

#### Docker Setup

If you prefer running it in a containerized environment:

1. Build the Docker image:
    ```bash
    docker build -t hello_docker .
    ```

2. Run the container:
    ```bash
    docker run -p 5000:5000 hello_docker
    ```

#### Deploying on Render
1. Go to [Render](https://render.com/), sign up, and create a new web service.
2. Link your GitHub repository to the service.
3. Choose a **Docker** service, specify your Dockerfile and deploy.
4. Set environment variables for Redis:
    - `REDIS_HOST=redis`
    - `REDIS_PORT=6379`

---

### Technologies Used:
- **Flask**: Python web framework for building the backend.
- **Speedtest-cli**: A Python library to test internet speeds.
- **Flask-Limiter**: For rate limiting API requests.
- **Gunicorn**: Production-ready server to run the Flask app.
- **Redis**: In-memory store for rate-limiting.
- **Chart.js**: For graphical representation of speed data.
- **Docker**: For containerizing the application and dependencies.
- **Render**: For cloud deployment.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

