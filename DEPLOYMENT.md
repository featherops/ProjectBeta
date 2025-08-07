# Hugging Face Spaces Deployment Guide

This guide will walk you through deploying the Nekros application to Hugging Face Spaces.

## Prerequisites

1.  A Hugging Face account.
2.  A Git repository (e.g., on GitHub) containing the code from this project, including the `Dockerfile`.

## Deployment Steps

1.  **Log in to Hugging Face:** Go to [huggingface.co](https://huggingface.co) and log in to your account.

2.  **Create a New Space:**
    *   Click on your profile picture in the top right corner and select "New Space".
    *   Give your Space a name.
    *   Select a license (e.g., MIT).
    *   Under "Space SDK", select **"Docker"**.
    *   Choose the "Blank" template.
    *   You can choose the hardware resources. The free tier should be sufficient for this application.
    *   Click "Create Space".

3.  **Upload Your Code:**
    *   Once your Space is created, you will be taken to its page. You will see instructions on how to upload your files.
    *   The easiest way is to use Git. Follow the instructions to clone your new Space repository, add your files, commit, and push.
    *   Your repository should look like this:
        ```
        .
        ├── Dockerfile
        ├── Ransomeware/
        ├── app/
        ├── api/
        └── ... (other files)
        ```
    *   Push your code to the `main` branch of your Space repository.

4.  **Building and Running:**
    *   After you push your code, Hugging Face Spaces will automatically start building the Docker image from your `Dockerfile`.
    *   You can see the build logs in the "Logs" tab of your Space.
    *   If the build is successful, the application will start automatically. The `start.sh` script will run, starting both the Flask API and the Next.js frontend.

5.  **Accessing Your Application:**
    *   Once the application is running, you will see it embedded in your Hugging Face Space page.
    *   The Next.js frontend will be available at the main URL of your Space.
    *   The Flask API will be running in the background and will be accessible to the frontend at the same origin, so the `/generate` endpoint should work as expected.

That's it! Your Nekros application should now be running on Hugging Face Spaces.
