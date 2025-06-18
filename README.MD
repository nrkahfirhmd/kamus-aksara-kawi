# Installation and Usage Guide: Kawi Dictionary App

This tutorial will guide you through the entire process of running the Kawi Dictionary App, from setting up the SPARQL database server to running the web application with Streamlit.

### **No Installation Option**
This application is fully hosted with a fuseki-server in Google Cloud VM Instance.
Just visit the [kamus-aksara-kawi.streamlit.app](https://kamus-aksara-kawi.streamlit.app/)


### **Prerequisites**

Before starting, ensure you have the following software installed:

1. **Python** (version 3.7 or newer).
2. **Java** (required to run Apache Jena Fuseki).
3. An RDF/Turtle data file for your Kawi dictionary (e.g., `pratisentana.ttl`).

---

### **Step 1: Set Up the Apache Jena Fuseki Server**

This application requires a SPARQL server to query your dictionary data. We will use Apache Jena Fuseki.

1. **Download Apache Jena Fuseki:**
   * Visit the [official Apache Jena download page](https://jena.apache.org/download/).
   * Download the `.zip` or `.tar.gz` file for "Apache Jena Fuseki".

2. **Extract and Run the Server:**
   * Extract the downloaded file to a directory of your choice.
   * Open a terminal or command prompt and navigate to the newly extracted Fuseki directory.
   * Run the server with the following command:
     ```bash
     # For Windows
     fuseki-server.bat
     
     # For macOS/Linux
     ./fuseki-server
     ```
   * Once the server is running, you will see output indicating that it's active at `http://localhost:3030`.

3. **Create a New Database:**
   * Open your web browser and go to `http://localhost:3030`.
   * Click the **manage datasets** tab, then select **add new dataset**.
   * Enter a dataset name, for example, **`pratisentana1`**. Make sure this name exactly matches the `FUSEKI_ENDPOINT` variable in the Python script.
   * Select **`In-memory`** as the dataset type and click **Create dataset**.

4. **Upload Your Dictionary Data:**
   * After the dataset is created, click its name (`pratisentana1`) from the list.
   * Select the **upload files** tab.
   * Click **Select file(s)...** and choose your Kawi dictionary RDF/Turtle file (e.g., `pratisentana.ttl`).
   * Click **upload all** to upload the data to the server.

Your Fuseki server is now ready and contains the necessary dictionary data.

---

### **Step 2: Set Up the Python Environment**

It is highly recommended to use a virtual environment to keep project dependencies isolated.

1. **Create a Project Directory:**
   * Create a new folder for your project and navigate into it using your terminal.
   * Place the Python script from the Canvas inside this directory and save it with a name (e.g., `app.py`).

2. **Create and Activate a Virtual Environment:**
   * Run the following command in your terminal:
     ```bash
     # Creates a virtual environment named 'venv'
     python -m venv venv
     ```
   * Activate the environment:
     ```bash
     # For Windows
     .\venv\Scripts\activate
     
     # For macOS/Linux
     source venv/bin/activate
     ```
   * You will see `(venv)` at the beginning of your terminal prompt, indicating the virtual environment is active.

---

### **Step 3: Install Python Dependencies**

With the virtual environment active, install all the required Python libraries.

* Run the following command in your terminal:
  ```bash
  pip install streamlit SPARQLWrapper pandas
  ```

---

### **Step 4: Run the Streamlit Application**

Everything is now set up. Make sure your Fuseki server is still running.

1. **Run the App:**
   * In your terminal (with the virtual environment still active), run the command:
     ```bash
     streamlit run app.py
     ```
   * (*Replace `app.py` if you named your Python script something else.*)

2. **Open in Browser:**
   * Streamlit will automatically open a new tab in your browser pointing to the running application, usually at `http://localhost:8501`.
   * You can now interact with the Kawi Dictionary, using the virtual keyboard to translate script or by entering Latin text.

Congratulations! You have successfully installed and launched the Kawi Dictionary App.
