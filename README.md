# Dondig's Wildlife Seminary - Australian Wildlife Education Platform

An interactive educational platform designed for children to learn about Australian native wildlife, conservation, and environmental protection through engaging games and data visualizations.

![Wildlife Seminary](https://img.shields.io/badge/Vue.js-3.4.0-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Overview

Dondig's Wildlife Seminary is an educational web application that helps children learn about Australian endangered species through interactive games, data visualization, and storytelling. The platform addresses the critical need for wildlife conservation awareness among young audiences.

**Target Audience:** Children (primary school level) and their parents

**Mission:** Increase children's awareness of Australia's native endangered species and foster environmental responsibility through AI-driven tools and interactive learning.

## Features

### Interactive Wildlife Map (Learn Wildlife)
- Real-time wildlife observation data visualization using Mapbox GL
- Filter by conservation status, season, and location
- Click on map markers to view detailed species information
- Dynamic clustering for better performance with large datasets

### Seasonal Wildlife Activities
- Explore animal behaviors across four seasons (Spring, Summer, Autumn, Winter)
- Interactive data cards showing:
  - Active species per season
  - Activity time distribution (Morning, Afternoon, Evening, Night)
  - Top 10 animals for each season
  - Seasonal comparison charts

### AI Animal Challenge
- Interactive guessing game where AI tries to identify the animal you're thinking of
- Question-based decision tree algorithm
- Educational animal facts and conservation status information
- Wikipedia integration for animal images

### Daily Wildle
- Daily animal guessing challenge
- Progressive hint system with up to 10 attempts
- Auto-complete species search
- Animal detail cards with conservation information

### Audio Matching Game
- Learn to recognize Australian animal sounds
- 5-round matching game with visual feedback
- Wikipedia image integration for species recognition
- Score tracking and educational content

### Yearly Population Analysis
- Time-series analysis of species populations
- Story-based data presentation for children
- Interactive accordion timeline
- Trend visualization with educational context
- Year-over-year comparison

### Conservation Matters
- Information about endangered species
- Conservation tips for children
- Climate change impact education
- Links to conservation organizations

## Technology Stack

### Frontend
- **Vue.js 3** - Progressive JavaScript framework with Composition API
- **Vue Router 4** - Client-side routing
- **Vite 5** - Modern build tool and dev server
- **Mapbox GL JS 3.14** - Interactive map visualization
- **Three.js 0.167** - 3D graphics rendering
- **JavaScript ES6+** - Modern JavaScript features
- **HTML5 & CSS3** - Semantic markup and advanced styling
  - CSS Grid & Flexbox for layouts
  - CSS Animations & Transitions
  - Responsive design with media queries

### Backend
- **Python 3.11** - Server-side programming
- **Flask** - Lightweight web framework
- **Flask-CORS** - Cross-Origin Resource Sharing support
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Relational database (via Render)
- **Gunicorn** - WSGI HTTP server
- **python-dotenv** - Environment variable management
- **pytz** - Timezone calculations

### APIs & External Services
- **Wikipedia REST API** - Animal images and information
- **Render** - Cloud hosting platform
  - Backend deployment
  - PostgreSQL database hosting
- **Mapbox API** - Map tiles and geolocation services

### Development Tools
- **Git** - Version control
- **GitHub** - Code repository and collaboration
- **npm** - JavaScript package manager
- **pip** - Python package manager
- **IntelliJ IDEA** - Integrated development environment

## Project Structure

```
FIT5120-MainProject/
├── frontend/                 # Vue.js frontend application
│   ├── src/
│   │   ├── pages/           # Page components
│   │   │   ├── Home.vue
│   │   │   ├── LearnWildlife.vue
│   │   │   ├── SeasonalPage.vue
│   │   │   ├── AIChallenge.vue
│   │   │   ├── DailyWildle.vue
│   │   │   ├── AudioMatchingGame.vue
│   │   │   ├── YearlyAnalysis.vue
│   │   │   └── Conservation.vue
│   │   ├── components/      # Reusable Vue components
│   │   │   ├── wildlife/    # Wildlife-specific components
│   │   │   ├── seasonal/    # Seasonal feature components
│   │   │   ├── ai/          # AI challenge components
│   │   │   ├── audio/       # Audio game components
│   │   │   ├── yearly/      # Yearly analysis components
│   │   │   └── common/      # Shared components
│   │   ├── router/          # Vue Router configuration
│   │   ├── services/        # API service layer
│   │   ├── utils/           # Utility functions
│   │   └── assets/          # Static assets
│   ├── public/              # Public static files
│   │   └── images/          # Image assets
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
│
├── backend/                 # Flask backend application
│   ├── app.py              # Main Flask application
│   ├── routes/             # API route handlers
│   │   ├── season.py       # Seasonal wildlife endpoints
│   │   ├── map.py          # Map data endpoints
│   │   ├── species.py      # Species information endpoints
│   │   ├── ai_challenge.py # AI challenge game logic
│   │   ├── daily_wildle.py # Daily guessing game
│   │   ├── audio.py        # Audio matching game
│   │   ├── yearly.py       # Yearly analysis endpoints
│   │   ├── conservation.py # Conservation information
│   │   ├── top.py          # Top species endpoints
│   │   └── trends.py       # Trend analysis endpoints
│   ├── lib/                # Shared libraries
│   │   └── db.py          # Database helper functions
│   ├── data/              # Data processing and datasets
│   │   ├── dataset/       # CSV data files
│   │   │   ├── Epic1/     # Map feature data
│   │   │   ├── Epic2/     # Seasonal data
│   │   │   ├── Epic5/     # Conservation data
│   │   │   ├── Epic6/     # Yearly analysis data
│   │   │   └── iteration3-sound/ # Audio game data
│   │   └── *.ipynb        # Data processing notebooks
│   ├── static/            # Static audio files
│   │   └── *.mp3         # Animal sound files
│   ├── requirements.txt   # Python dependencies
│   └── *.sql             # Database schema and setup scripts
│
└── README.md             # This file
```

## Getting Started

### Prerequisites

- **Node.js** (v18 or higher)
- **npm** (v9 or higher)
- **Python** (v3.11 or higher)
- **pip** (latest version)
- **PostgreSQL** (v14 or higher) - optional for local development

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/your-username/FIT5120-MainProject.git
cd FIT5120-MainProject
```

#### 2. Frontend Setup

```bash
cd frontend
npm install
```

Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:5000
VITE_MAPBOX_TOKEN=your_mapbox_access_token
```

#### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://user:password@host:port/database
FLASK_ENV=development
FLASK_APP=app.py
```

#### 4. Database Setup

Run the SQL scripts to create tables:

```bash
psql -h your-host -U your-user -d your-database -f database_schema.sql
psql -h your-host -U your-user -d your-database -f create_map_tables.sql
psql -h your-host -U your-user -d your-database -f create_yearly_table.sql
```

### Running the Application

#### Development Mode

**Frontend (runs on http://localhost:3000):**
```bash
cd frontend
npm run dev
```

**Backend (runs on http://localhost:5000):**
```bash
cd backend
python app.py
```

#### Production Build

**Frontend:**
```bash
cd frontend
npm run build
npm run preview
```

**Backend:**
```bash
cd backend
gunicorn app:app
```

## API Documentation

### Base URL
- **Development:** `http://localhost:5000/api`
- **Production:** `https://fit5120-backend.onrender.com/api`

### Endpoints

#### Seasonal Wildlife
- `GET /season/kpi` - Get KPI data for all seasons
- `GET /season/activity` - Get activity time distribution by season
- `GET /season/top-animals` - Get top 10 animals per season

#### Wildlife Map
- `GET /map/observations` - Get wildlife observations with filters
  - Query params: `status`, `season`, `limit`

#### Species Information
- `GET /species/search?q={query}` - Search species by name
- `GET /species/{id}` - Get detailed species information

#### AI Challenge
- `POST /ai-challenge/start` - Start new AI challenge game
- `POST /ai-challenge/answer` - Submit answer and get next question
- `GET /ai-challenge/guess` - Get AI's final guess

#### Daily Wildle
- `GET /daily-wildle/today` - Get today's challenge animal
- `POST /daily-wildle/guess` - Submit a guess
- `GET /daily-wildle/autocomplete?q={query}` - Get species suggestions

#### Audio Game
- `GET /audio/sounds` - Get all animal sounds
- `GET /audio/details/name/{name}` - Get animal details by name

#### Yearly Analysis
- `GET /yearly/species` - Get list of species with yearly data
- `GET /yearly/species/{id}/trend` - Get yearly population trend

#### Conservation
- `GET /conservation/species` - Get endangered species information

## Database Schema

### Main Tables

#### `wildlife_observations`
- Stores wildlife observation records
- Columns: `id`, `common_name`, `scientific_name`, `latitude`, `longitude`, `observed_on`, `conservation_status`, `season`

#### `species`
- Species master data
- Columns: `taxon_id`, `common_name`, `scientific_name`, `image_url`, `conservation_status`

#### `seasonal_kpi`
- Seasonal statistics
- Columns: `season`, `active_species`, `total_observations`

#### `animal_sounds`
- Animal sound files metadata
- Columns: `id`, `common_name`, `scientific_name`, `sound_url`

#### `animal_details`
- Detailed animal information
- Columns: `id`, `common_name`, `scientific_name`, `description`, `habitat`, `diet`, `threats`

#### `yearly_observations`
- Yearly population data
- Columns: `id`, `taxon_id`, `year`, `observation_count`

## Deployment

### Backend (Render)

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure build settings:
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Root Directory:** `backend`
4. Add environment variables:
   - `DATABASE_URL` - PostgreSQL connection string
   - `PYTHON_VERSION` - 3.11.9

### Frontend (Render Static Site)

1. Create a new Static Site on Render
2. Configure build settings:
   - **Build Command:** `cd frontend && npm install && npm run build`
   - **Publish Directory:** `frontend/dist`
3. Add environment variables:
   - `VITE_API_BASE_URL` - Backend API URL
   - `VITE_MAPBOX_TOKEN` - Mapbox access token

### Database (Render PostgreSQL)

1. Create a PostgreSQL instance on Render
2. Note the connection string
3. Run SQL scripts to set up tables
4. Import data using provided scripts

## Key Features Implementation

### Interactive Storytelling
The Yearly Analysis feature uses a unique storytelling approach to present data:
- Accordion-style timeline for year-by-year exploration
- Animated animal icons showing population counts
- Educational cards explaining trends in child-friendly language
- Color-coded borders indicating growth (green) or decline (red)

### Real-time Data Visualization
- Dynamic map clustering for 10,000+ observations
- Responsive charts that adapt to different screen sizes
- Live filtering and search functionality

### Educational Gaming
- Progressive difficulty in AI Challenge
- Daily rotation for Daily Wildle
- Audio recognition training
- Immediate feedback and explanations

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- **Frontend:** Follow Vue.js style guide and ESLint rules
- **Backend:** Follow PEP 8 Python style guide
- **Commits:** Use conventional commit messages

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Team

**IT DOG Team**
- Project developed for FIT5120 - Industry Experience Project
- Monash University, 2025

## Acknowledgments

- **Data Source:** Atlas of Living Australia (ALA)
- **Map Services:** Mapbox
- **Animal Information:** Wikipedia API
- **Icons:** Icons8, Flaticon
- **Hosting:** Render

## Contact

For questions or support, please open an issue on GitHub.

---

**Made with care for Australian Wildlife Conservation**
