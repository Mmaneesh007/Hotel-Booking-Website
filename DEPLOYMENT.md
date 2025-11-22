# Deploying Hospitality AI to Streamlit Cloud

Since this is a Streamlit application, the easiest way to make it public is using **Streamlit Community Cloud**. It's free and connects directly to your GitHub repository.

## Prerequisites
1.  A **GitHub Account**.
2.  A **Streamlit Cloud Account** (you can sign up using your GitHub account).

## Steps to Deploy

### 1. Push Code to GitHub
First, you need to put this code into a GitHub repository.
1.  Initialize a git repo in this folder:
    ```bash
    git init
    git add .
    git commit -m "Initial commit of Hospitality AI"
    ```
2.  Create a new repository on GitHub.
3.  Push your code:
    ```bash
    git remote add origin <your-repo-url>
    git branch -M main
    git push -u origin main
    ```

### 2. Deploy on Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **"New app"**.
3.  Select your GitHub repository (`hospitality_ai`).
4.  Set the **Main file path** to `app.py`.
5.  Click **"Deploy!"**.

### 3. Access Your App
Once deployed, Streamlit will give you a public URL (e.g., `https://hospitality-ai.streamlit.app`) that you can share with anyone!

## Notes
- **Database**: The app uses a local SQLite database (`hotel_inr.db`). On Streamlit Cloud, this database will be recreated each time the app restarts (which is fine for a demo).
- **Images**: The `images/` folder is included in the repo, so your room previews will work automatically.
