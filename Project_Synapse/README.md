# Project Synapse: Autonomous AI Agent for Last-Mile Delivery

## Overview

Project Synapse introduces an autonomous AI agent designed to intelligently handle and resolve complex disruptions in last-mile delivery logistics. Unlike traditional rule-based systems, this agent leverages human-like reasoning to proactively address issues such as restaurant delays, traffic incidents, package disputes, and recipient unavailability, ensuring smoother operations and enhanced customer satisfaction.

The core idea is to demonstrate how an AI agent, powered by an LLM (though simulated here), can interact with various "tools" (mimicking real-world APIs) to gather information, make decisions, and execute multi-step plans to resolve dynamic scenarios.

## Features

*   **Scenario-Based Handling**: Automatically detects and processes different types of delivery disruptions (e.g., "restaurant delay", "traffic", "damaged package", "recipient unavailable").
*   **Transparent Decision Logging**: Utilizes a `DecisionLog` to record every step the agent takes, including "what" was done, "why" it was done, and the "result" of the action, providing full transparency into the agent's reasoning process.
*   **Proactive Problem Solving**: Implements specific strategies for various scenarios:
    *   **Restaurant/Kitchen Delays**: Checks merchant status, notifies customers with vouchers, re-routes drivers, and suggests alternatives.
    *   **Traffic/Accident Issues**: Checks traffic, calculates alternative routes, and informs passengers.
    *   **Damaged Package/Disputes**: Initiates mediation, collects evidence, analyzes fault, issues refunds, exonerates drivers, and logs merchant feedback.
    *   **Recipient Unavailable**: Attempts chat contact, and if no response, finds nearby lockers or reschedules delivery.
*   **Simulated Tool Integration**: Interacts with a set of mock API functions (defined in `tools.py`) that simulate real-world logistics operations.

## Project Structure

*   `agent.py`: The main script containing the `Agent` class, which orchestrates the scenario handling and decision-making process. It also includes the `DecisionLog` for logging the agent's actions.
*   `tools.py`: A collection of Python functions that simulate external API calls to various logistics services (e.g., checking merchant status, re-routing drivers, notifying customers). These functions use data from `mock_data.json`.
*   `mock_data.json`: A JSON file containing sample data for merchants, drivers, traffic routes, and lockers, used by the `tools.py` functions.

## Getting Started

### Running the Agent

The agent runs in an interactive command-line mode, allowing you to input different scenarios.

1.  **Navigate to the `MultipleFiles` directory:**
    ```bash
    cd MultipleFiles
    ```
2.  **Run the `agent.py` script:**
    ```bash
    python agent.py
    ```

3.  **Interact with the agent:**
    The program will prompt you to "Enter scenario:". Type a scenario description (e.g., "restaurant delay", "traffic accident", "damaged package", "recipient not home") and press Enter.
    Type `quit` or `exit` to end the program.

    **Example Scenarios to Try:**
    *   `There's a delay at the kitchen.`
    *   `We hit traffic on the way.`
    *   `The package arrived damaged.`
    *   `The recipient is not home.`
    *   `The customer is unavailable for delivery.`

## How it Works (Conceptual)

The `Agent` class in `agent.py` acts as the central orchestrator. When `handle_scenario` is called, it analyzes the input string to identify keywords that match predefined disruption types. Based on the identified type, it calls a specific private method (e.g., `_handle_restaurant_delay`).

Each handling method then uses functions from `tools.py` to simulate interactions with external systems. The `DecisionLog` meticulously records each "tool call," its purpose, and the simulated result, providing a clear audit trail of the agent's thought process and actions.

While this implementation uses a rule-based approach for scenario matching and a fixed sequence of tool calls, it lays the groundwork for integrating more advanced LLM capabilities for dynamic reasoning and tool selection.

## Future Enhancements

*   **LLM Integration**: Replace the rule-based scenario handling with an actual LLM to interpret natural language inputs more flexibly and generate dynamic action plans.
*   **Dynamic Tool Selection**: Allow the LLM to choose the most appropriate tools from `tools.py` based on the current context and desired outcome, rather than following a fixed sequence.
*   **Feedback Loop**: Implement a mechanism for the agent to learn from the outcomes of its actions and refine its strategies over time.
*   **More Complex Scenarios**: Expand the range of scenarios the agent can handle, including multi-faceted problems requiring coordination across several domains.
*   **User Interface**: Develop a simple web-based or graphical user interface for easier interaction.
