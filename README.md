# Data Flow Anomaly Detector

This program is designed to detect various anomalies in the flow of data within a codebase. It analyzes C++ code snippets and identifies potential issues related to variable usage, initialization, referencing, and more. Below is a breakdown of the functionality provided by this detector.

## Features

- **Double Operators Handling:** This detector identifies and converts double operators like '++', '--', '+=', '-=', '*=', '/=' to their respective equivalent operations for improved code readability and understanding.

- **Variable Tracking:** It tracks the usage, initialization, and referencing of variables throughout the code to detect anomalies such as undefined variables, redefinitions, and variables defined but not referenced.

- **Keyword and Data Type Handling:** Certain keywords and data types are treated specially, ensuring their correct usage and adherence to coding standards.

## Usage

To utilize the Data Flow Anomaly Detector, follow these steps:

1. **Input:** Provide the code snippet to be analyzed in an Input File. The detector parses the code and performs various checks to identify anomalies.

2. **Anomaly Detection:** The detector scans the code for anomalies such as undefined variables, redefinitions, variables defined but not referenced, and more.

3. **Output:** Anomalies are reported along with their context in the code, aiding developers in understanding and rectifying potential issues.

