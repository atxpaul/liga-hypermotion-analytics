# LaLiga Hypermotion Analytics Project

Welcome to the **LaLiga Hypermotion Analytics Project**, an advanced analytics tool designed to provide insights into various metrics of LaLiga Hypermotion teams, such as cost per goal and stadium attendance rates. This project combines data visualization with geographic analytics to offer a detailed view of performance and audience engagement across different teams and cities.

## Table of Contents

-   [Overview](#overview)
-   [Features](#features)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Project Structure](#project-structure)
-   [Data Sources](#data-sources)
-   [Future Enhancements](#future-enhancements)
-   [Contributors](#contributors)

## Overview

This project is a comprehensive analytics dashboard focused on LaLiga Hypermotion, utilizing data such as team budgets, player costs, goals scored, population metrics, and stadium attendance. With visualizations, including bar charts and bubble maps, we provide a better understanding of team efficiencies and the relationship between audience attendance and city population.

## Features

-   **Cost per Goal Visualization**: A bar chart ranking teams by their "cost per goal" metric, which indicates the investment efficiency of each team.
-   **Stadium Attendance Analysis**: A map-based bubble chart that compares the average attendance for each team to the population of the city where they play. This gives insights into audience engagement by showing attendance as a percentage of the local population.
-   **Geolocation Integration**: Fetches coordinates for each team's city using the Nominatim API, allowing for a visually compelling geographic display.
-   **Color-Coded Metrics**: Attendance rate percentages are color-coded for quick insights, with larger bubbles representing higher attendance figures.

## Installation

1. **Clone the repository**:

    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2. **Install dependencies**:
   Ensure you have Python 3.x installed, then install required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. **Data Preparation**:

    - Place `table_budgetxplayers.csv` and `table_popxmunixequipo.csv` files in the appropriate directories, or modify the import paths in the code if needed.

4. **Map API Setup**:
   The project uses the Nominatim API to retrieve geographical coordinates for city names. This API has usage limitations, so consider implementing rate limiting if processing large datasets.

## Usage

Run the main script to generate the dashboards:

```bash
python main.py
```

This will display two separate dashboards:

1. **Cost per Goal Dashboard**: Ranks each team based on the cost per goal, providing an ordered bar chart of teams.
2. **Stadium Attendance Dashboard**: Displays a bubble map of attendance data by city, with the bubble size representing attendance and color representing the percentage of the city population attending.

### Code Overview

-   `fig1`: Bar chart of teams ordered by "cost per goal."
-   `fig2`: Bubble map with attendance information.

### Dashboard Details

#### Cost per Goal

This chart ranks teams based on the total cost per goal scored. Teams that achieve more goals with a lower total budget appear higher, representing a more efficient investment.

#### Stadium Attendance

This map displays the average attendance for each team's home games as a percentage of the local population. Cities with a high percentage of attendees indicate strong local support relative to the population.

## Data Sources

-   **Team Budget and Goals**: Stored in `table_budgetxplayers.py`, this dataset includes financial data and goals scored by each team.
-   **Population and Attendance**: Stored in `table_popxmunixequipo.py`, this dataset provides city population and stadium attendance for each team.

## Future Enhancements

-   **Additional Metrics**: Incorporate metrics like cost per player, average salary per goal, and player-specific performance analytics.
-   **Real-time Data**: Add support for real-time or regularly updated data from LaLiga sources.
-   **Historical Analysis**: Extend the dataset to cover multiple seasons for trend analysis.
-   **Advanced Interactivity**: Improve user interaction in the dashboard with filters for specific teams, cities, or metrics.

## Contributors

This project was created with the collaborative efforts of the following people:

-   [**@atxpaul**](https://github.com/atxpaul) - DevOps and Software Engineer
-   [**@Sofia-A-Fayo-Freites**](https://github.com/Sofia-A-Fayo-Freites) - Data Analyst
-   [**@samtlme**](https://github.com/samtlme) - FullStack Engineer

Special thanks to everyone involved in making this project a success!

## License

This project is licensed under the MIT License.

## Contact

For questions or further information, please reach out to the project maintainer.

---

Enjoy exploring the insights provided by the LaLiga Hypermotion Analytics Project!
