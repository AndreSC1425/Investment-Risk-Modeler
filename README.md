# Investment Risk Modeler: Monte Carlo Analysis

## Project Overview

This is an application designed to analyze the financial risk of a user-defined investment portfolio using modeling.

### Features
* **User Input:** Accepts multiple stock tickers and custom weight allocations.
* **Monte Carlo Simulation:** Runs 5,000 simulations over a 5-year horizon to project portfolio returns.
* **Risk Metrics:** Calculates the **Compound Annual Growth Rate (CAGR)** and **Value at Risk (VaR)** at the 95th percentile.
* **Visualization:** Displays the probability distribution of final portfolio values using an interactive histogram.

---

## Technology Stack

| &nbsp; | &nbsp; | &nbsp; |
| :--- | :--- | :--- |
| **Frontend (UI)** | **Angular** | User input and data visualization (Histogram). |
| **Backend (API)** | **Spring Boot (Java)** | REST Controllers |
| **Python** | Pandas, NumPy, SciPy, `yfinance` | Executes the Monte Carlo Simulation and financial modeling. |

---

## Setup and Running Locally

To run this application, you need **Java, Maven, Node.js (with Angular CLI),** and **Python**.

### 1. Backend Setup (Spring Boot & Python)

1.  **Navigate to the root directory:**
    ```bash
    cd PortfolioDeconstructor
    ```

2.  **Activate Python Virtual Environment:**
    ```bash
    .\python_engine\venv\Scripts\activate
    ```

3.  **Run the Spring Boot API:** This command starts the Java application, which will run on `http://localhost:8080`.
    ```bash
    # Ensure you are in the 'spring/demo' folder before running:
    cd spring/demo
    mvn spring-boot:run
    ```

### 2. Frontend Setup (Angular)

1.  **Open a NEW Terminal** (keep the backend running in the first terminal).
2.  **Navigate to the Angular directory:**
    ```bash
    cd risk-deconstructor-ui
    ```

3.  **Start the Angular Development Server:**
    ```bash
    ng serve --open
    ```
    This will open the application in your browser (`http://localhost:4200`).

---

## How to Use the Application

1.  Enter stock tickers.
2.  Adjust the percentages to ensure **Total Weight** is **100%**.
3.  Click **"Run Monte Carlo Analysis"**.
4.  The Angular frontend sends the request to the **Spring Boot API**.
5.  The **Spring Boot API** executes the **Python** script.
6.  Results (CAGR, VaR, and the distribution histogram) are displayed on the screen.
