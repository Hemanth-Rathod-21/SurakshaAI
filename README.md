# SurakshaAI V1

AI-Powered Digital Safety Companion for Elderly People.

Tagline: Pause. Check. Stay Safe.

## V1 scope
- Message Checker
- Link Checker
- Simple risk levels: Lower Risk / Caution / High Risk
- Explanation of warning indicators
- Safe next-step guidance
- Logistic Regression text classifier

## Run in VS Code / PowerShell

1. Open this folder in VS Code.
2. Create a virtual environment:

   python -m venv .venv

3. Activate it:

   .\.venv\Scripts\Activate.ps1

4. Install packages:

   pip install -r requirements.txt

5. Train the initial model:

   python train_model.py

6. Start the website:

   python app.py

7. Open:

   http://127.0.0.1:5000

## Important
This is a prototype. A "Lower Risk" result does NOT prove that a message or website is genuine.
Never enter real OTPs, PINs, passwords, card numbers or banking credentials into the prototype.
