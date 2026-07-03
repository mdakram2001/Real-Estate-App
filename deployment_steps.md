# Gurgaon Real Estate Portal: Deployment Steps & Troubleshooting Log

This document lists all the steps taken to deploy the Streamlit application to the **DigitalOcean App Platform**, the issues encountered during the process, and how they were resolved.

---

## 🛠️ Summary of Deployment Steps

### 1. Port Configuration
* Created a [.streamlit/config.toml](file:///c:/Users/HP/Desktop/Capstone%20Project/Data%20Cleaning/dsmp-capstone-project/App/.streamlit/config.toml) file in the root directory to define the container port and bind address:
  ```toml
  [server]
  port = 8080
  address = "0.0.0.0"
  headless = true
  enableCORS = false
  enableXsrfProtection = false
  ```

### 2. DigitalOcean App Platform Configuration
* Connected the GitHub repository to DigitalOcean.
* Set the component's **Public HTTP port** to `8080` (matching the `config.toml` file).
* Configured the resource size to **Basic (2 GB RAM / 1 vCPU)** since loading a 147 MB machine learning pipeline alongside visual analytics and pandas dataframes will exceed the limits of a 512 MB or 1 GB RAM instance.
* Set the **Run command** to:
  ```bash
  streamlit run Home.py --server.port 8080 --server.address 0.0.0.0
  ```

---

## ⚠️ Problems Faced and Resolutions

### Problem 1: Large Files (>100MB) Rejected by GitHub
* **Symptoms:** Pushing changes failed because `datasets/pipeline.pkl` (147.3 MB) exceeded GitHub's 100 MB file limit.
* **Resolution:**
  1. Initialized Git Large File Storage (LFS):
     ```bash
     git lfs install
     ```
  2. Registered tracking patterns relative to the current directory:
     ```bash
     git lfs track "datasets/*.pkl"
     ```

### Problem 2: Git Push Rejected due to Commited Large-File History
* **Symptoms:** Even after enabling Git LFS, pushing was rejected by the GitHub pre-receive hook because the large file was already committed as a standard Git blob in a previous local commit history.
* **Resolution:**
  1. Reset the local branch pointer back to the remote repository state (without losing local changes):
     ```bash
     git reset origin/main
     ```
  2. Re-staged and re-committed the changes so that the file was processed as an LFS pointer from the start of the commit:
     ```bash
     git add .gitattributes .gitignore .streamlit/ datasets/
     git commit -m "Add datasets, streamlit config, and models using Git LFS"
     git push origin main
     ```

### Problem 3: "invalid load key, 'v'" Error on Startup
* **Symptoms:** When viewing the deployed app in the browser, all pages crashed with: `Error loading recommender datasets: invalid load key, 'v'`. This happens because Python's pickle module read the Git LFS pointer text file (which begins with `version https://...`) instead of the actual model binary data.
* **Resolution:**
  1. Updated the **Build command** under the component settings in the DigitalOcean dashboard to:
     ```bash
     git lfs install && git lfs pull
     ```
  2. This forces the DigitalOcean build container to fetch the actual binary files from the LFS storage backend during the build process.

### Problem 4: Missing Pickle Dependencies in `requirements.txt`
* **Symptoms:** The app failed to build/run with errors:
  * `ModuleNotFoundError: No module named 'sklearn'` (required to unpickle and load the pipeline models)
  * `ModuleNotFoundError: No module named 'category_encoders'` (required by custom encoders in the pipeline)
  * Missing visual plotting helper library (`seaborn`) requested for display layout support.
* **Resolution:**
  * Updated [requirements.txt](file:///c:/Users/HP/Desktop/Capstone%20Project/Data%20Cleaning/dsmp-capstone-project/App/requirements.txt) to include all required backend dependencies:
    ```
    matplotlib==3.11.0
    numpy==2.5.0
    pandas==2.3.2
    plotly==6.3.1
    streamlit==1.49.1
    wordcloud==1.9.6
    scikit-learn
    category_encoders
    seaborn
    ```
  * Committed and pushed the changes to GitHub. DigitalOcean automatically detected the new commit and rebuilt the environment with all missing modules.
