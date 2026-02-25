---
title: NZ Louis Property API
emoji: 🏠
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: apache-2.0
---

# 🏠 NZ Louis Property API

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![HF Spaces](https://img.shields.io/badge/🤗-Hugging%20Face%20Spaces-yellow)](https://huggingface.co/spaces/NZLouislu/nzlouis-property-api)

High-Performance New Zealand Property Data API Service

## ✨ Features

- 🚀 **High Performance**: FastAPI-based async API with 20-60ms response time
- 🏡 **Comprehensive Data**: Coverage of major New Zealand regions including Auckland and Wellington
- 🔮 **AI Predictions**: Property price trend forecasting and sales probability analysis
- 📊 **Real-time Queries**: Multi-dimensional search by city, suburb, address, and more
- 🌐 **Auto Documentation**: Interactive API docs auto-generated with OpenAPI/Swagger
- 🎯 **Type Safety**: Pydantic data validation ensuring data quality
- 💾 **Database**: Integrated CockroachDB (distributed PostgreSQL)
- 🆓 **Free Deployment**: Hosted on Hugging Face Spaces with zero operational cost

## 📺 Live Demo

- **API Documentation**: [https://NZLouislu-nzlouis-property-api.hf.space/docs](https://NZLouislu-nzlouis-property-api.hf.space/docs)
- **ReDoc Documentation**: [https://NZLouislu-nzlouis-property-api.hf.space/redoc](https://NZLouislu-nzlouis-property-api.hf.space/redoc)
- **Health Check**: [https://NZLouislu-nzlouis-property-api.hf.space/health](https://NZLouislu-nzlouis-property-api.hf.space/health)

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone https://github.com/NZLouislu/nzlouis-property-api.git
cd nzlouis-property-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your CockroachDB credentials

# Start development server
uvicorn app.main:app --reload --port 8000

# Visit http://localhost:8000/docs to view API documentation
```
