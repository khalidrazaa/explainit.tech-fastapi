# In your project folder (where Dockerfile is), run:
docker build -t explainit-fastapi:local .

# -t explainit-fastapi:local → this is your local image tag.
# . → context is current directory.

# Render uses the $PORT environment variable, so locally we can simulate it. For example:
docker run -it --rm -p 8000:10000 -e PORT=10000 explainit-fastapi:local

# Explanation:
# -p 8000:10000 → map container port 10000 to host port 8000.
# -e PORT=10000 → sets the PORT env variable inside the container (used by your CMD).
# --rm → removes the container when stopped.
# -it → interactive mode, so you can see logs.
# Then open in browser: http://localhost:8000


# 4️⃣ Optional: Override environment variables locally
# You can pass a .env file:
docker run --env-file .env -p 8000:10000 explainit-fastapi:local

# Test commands inside container (optional)
docker run -it --rm -e PORT=10000 explainit-fastapi:local /bin/bash

# This drops you into the container shell.
# You can check installed packages, DB connectivity, etc.
