### ✅ Project Setup Instructions

Follow the steps below to set up and run the project locally:

1. **Install Python 3.11**
   Download and install Python 3.11 from the official site: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Install `uv` (a fast Python workflow manager)**

   ```bash
   pip install uv
   ```

3. **Create a virtual environment using `uv`**

   ```bash
   uv venv
   ```

4. **Activate the virtual environment**

   * On Windows:

     ```bash
     .venv\Scripts\activate
     ```
   * On macOS/Linux:

     ```bash
     source .venv/bin/activate
     ```

5. **Install project dependencies**

   ```bash
   uv sync
   ```

6. **Create a `.env` file in the root directory**

   Add the following environment variable:

   ```env
   MONGODB_URI="your_mongodb_connection_string"
   ```

7. **Run the FastAPI server**

   ```bash
   uvicorn src.main:app --reload
   ```

8. **Access the API documentation**
   Open your browser and navigate to:
   [http://localhost:8000/docs](http://localhost:8000/docs)

---