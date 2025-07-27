# Podcast Tool
This is a Flask-based Docker container designed for making the archival and organization of MP3 files from a podcast significantly easier

## Features
- Upload MP3 files through a user-friendly web interface.
- Download uploaded files with a single click.
- Delete files directly from the interface.
- Persistent storage for uploaded files, even after container restarts.
- Dark-themed UI for a modern and clean look.

## Requirements
- Docker
- Python 3.9 (used in the container)

## Setup and Usage

### 1. Clone the Repository
```bash
git clone <repository-url>
cd podcastapp-config
```

### 2. Build the Docker Image
```bash
docker build -t podcastapp .
```

### 3. Run the Container
```bash
docker run -p 1123:1123 -v /path/to/config:/app/uploads podcastapp
```

- Access the app at http://localhost:1123
- Uploaded files will be stored in /uploads

## File Structure
podcastapp-config/ 
├── flaskr/ 
│ ├── init.py # Main Flask application 
│ ├── templates/ 
│ │ └── index.html # HTML template for the web interface 
├── uploads/ # Directory for uploaded files (mapped to host) 
├── dockerfile # Dockerfile for building the container 
├── README

## Example Docker Compose Configuration
Docker image:
  podcastapp:
    build:
      context: .
      dockerfile: dockerfile
    ports:
      - "1123:1123"
    container_name: podcastapp
    volumes:
      - /path/to/config:/app/uploads

## Contributing
### Key Sections:
1. **Features**: Highlights the app's functionality.
2. **Setup and Usage**: Explains how to build and run the app using Docker.
3. **File Structure**: Provides an overview of the project's organization.
4. **Environment Variables**: Mentions configurable paths.
5. **Docker Compose Example**: For users who prefer Docker Compose.
6. **Screenshots**: Placeholder for visuals (you can replace with actual screenshots).
7. **License and Contributing**: Encourages collaboration.

Let me know if you'd like to tweak anything!

## License
This project is licensed under the MIT License. ``````