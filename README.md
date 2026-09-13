# ✈️ YatraMind AI — Multi-Agent Travel Intelligence Platform

YatraMind AI is an AI-powered multi-agent travel planning platform that converts natural-language travel requests into personalized travel plans.

Instead of manually searching across multiple travel websites, YatraMind AI coordinates specialized AI agents to research flights, discover hotels, create itineraries, and generate a structured travel plan.

The system is built using **LangGraph, LangChain, Groq, FastAPI, Tavily, and AviationStack**.

---

## 🌍 Why YatraMind AI?

Travel planning usually requires switching between multiple platforms for:

- ✈️ Flights
- 🏨 Hotels
- 📍 Destinations
- 🗺️ Itineraries
- 💰 Budget planning

YatraMind AI brings these tasks together into a single AI-powered workflow.

The platform uses a **multi-agent architecture**, where each agent is responsible for a specific travel-planning task and LangGraph coordinates the entire process.

---

## ✨ Features

- ✈️ Flight information and route research using AviationStack
- 🏨 Hotel and accommodation research using Tavily
- 🧠 Multi-agent orchestration using LangGraph
- 🤖 LLM-powered travel planning using Groq
- 🗺️ Day-by-day itinerary generation
- 💰 Budget-aware travel recommendations
- 🇮🇳 India-focused destination and airport support
- 🌍 International travel support
- 🌐 FastAPI backend
- 💬 Simple and responsive web interface
- 💾 Conversation state persistence using PostgreSQL
- 📄 Travel plan PDF export
- 📋 Copy generated travel plans directly from the UI

---

## 🧠 Multi-Agent Architecture

YatraMind AI uses a sequential LangGraph workflow consisting of four specialized agents.

```text
                    User Travel Request
                            │
                            ▼
                    ┌─────────────────┐
                    │  Flight Agent   │
                    │                 │
                    │ Flight research │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Hotel Agent   │
                    │                 │
                    │ Hotel research  │
                    └────────┬────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Itinerary Agent     │
                  │                     │
                  │ Day-by-day planning │
                  └──────────┬──────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Final Agent    │
                    │                 │
                    │ Final formatting│
                    └────────┬────────┘
                             │
                             ▼
                    Personalized Trip Plan