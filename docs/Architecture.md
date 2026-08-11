# Production-Grade Realtime Architecture Specification

```text
xebia_document_search_platform/
│
├── .github/                             # CI/CD Automation Workflows
│   └── workflows/
│        └── ci-cd.yml                   # GitHub Actions Continuous Integration & Continuous Deployment Pipeline
│
├── docker-compose.yml                   # Multi-Container Local & Production Docker Compose Orchestration
│
├── k8s/                                 # Kubernetes Production Deployment Manifests
│   ├── configmap.yaml                   # Kubernetes Non-Sensitive System ConfigMap
│   ├── secret.yaml                      # Kubernetes Opaque Secrets (API Keys, DB Passwords)
│   ├── mysql-deployment.yaml            # MySQL Stateful Pod Deployment & Service
│   ├── backend-deployment.yaml          # FastAPI RAG Backend Deployment (Replicas, Probes, Resources)
│   ├── frontend-deployment.yaml         # Angular Frontend Nginx Deployment & ClusterIP Service
│   └── ingress.yaml                     # Nginx Ingress Controller Routing Rules
│
├── backend/
│   ├── main.py                          # FastAPI Production Application Entrypoint
│   ├── Dockerfile                       # Multi-stage Container Image Definition for Backend
│   │
│   ├── core/                            # System Core & Configuration Management
│   │   ├── config.py                    # Environment variable loader (.env)
│   │   ├── database.py                  # MySQL Connection Pool & Cursor Provider
│   │   ├── logger.py                    # Structured Logger (Console Stream & File Loggers)
│   │   ├── security.py                  # Default User Security Context & Authorization Rules
│   │   ├── middleware.py                # FastAPI CORS & Global Exception Middleware
│   │   ├── constants.py                 # System Thresholds, Expiry, Intent Definitions & Allowed Categories
│   │   ├── startup.py                   # Singleton Lifecycle Initializer (Pinecone, HuggingFace, CrossEncoder, BM25)
│   │   └── settings.py                  # Application Settings Configuration
│   │
│   ├── api/                             # API Presentation Layer
│   │   └── v1/
│   │        ├── routes/
│   │        │      ├── interview.py     # Main /ask POST endpoint router
│   │        │      ├── evaluation.py    # Evaluation API endpoints
│   │        │      ├── session.py       # Session history retrieval router
│   │        │      ├── health.py        # / and /health health check router
│   │        │      └── admin.py         # Admin status router
│   │        │
│   │        ├── schemas/
│   │        │      ├── interview_schema.py # QuestionRequest, QuestionResponse, Source, ApiResponse, ErrorResponse
│   │        │      ├── evaluation_schema.py# Evaluation API Pydantic schemas
│   │        │      └── session_schema.py   # Session history API Pydantic schemas
│   │        │
│   │        └── services/
│   │               ├── interview_service.py # High-Level RAG Execution & Orchestration Service
│   │               ├── evaluation_service.py# Evaluation Business Logic Service
│   │               └── session_service.py  # Session Management Service
│   │
│   ├── ai/                              # CrewAI Agentic Intelligence Engine
│   │   ├── agents/
│   │   │      ├── classifier_agent.py   # Enterprise HR Query Classifier Agent
│   │   │      ├── history_agent.py      # Conversation Context Query Rewriter Agent
│   │   │      ├── answer_agent.py       # Strict Enterprise HR Policy Assistant Agent
│   │   │      ├── planner_agent.py      # Technical Interview Topic Planner Agent
│   │   │      ├── question_agent.py     # Evaluation Question Generator Agent
│   │   │      ├── qa_agent.py           # Quality & Safety Assurance Auditor Agent
│   │   │      └── evaluator_agent.py    # Answer Scoring & Evaluation Agent
│   │   │
│   │   ├── tasks/
│   │   │      ├── question_task.py      # Classifier Task Kickoff Logic
│   │   │      ├── qa_task.py            # History Query Rewriter Task Kickoff Logic
│   │   │      ├── answer_task.py        # Answer Generator Task Kickoff Logic
│   │   │      ├── planner_task.py       # Planner Task Builder
│   │   │      └── evaluation_task.py   # Evaluation Task Builder
│   │   │
│   │   ├── crews/
│   │   │      ├── interview_crew.py     # HRRAGFlow Deterministic Execution Engine
│   │   │      └── evaluation_crew.py    # Evaluation Crew Orchestration Engine
│   │   │
│   │   ├── prompts/
│   │   │      ├── classifier_prompt.py  # Query Classification Prompts & Allowed Taxonomy
│   │   │      ├── history_prompt.py     # History Query Rewrite Rules & Prompts
│   │   │      ├── answer_prompt.py      # Context-Grounded Answer Generation Prompts
│   │   │      ├── planner_prompt.py     # Interview Planning Prompts
│   │   │      ├── question_prompt.py    # Question Generation Prompts
│   │   │      ├── qa_prompt.py          # Quality Assurance Prompts
│   │   │      └── evaluation_prompt.py  # Response Evaluation Prompts
│   │   │
│   │   ├── llm/
│   │   │      ├── llm_factory.py        # Dynamic LLM Provider Factory
│   │   │      ├── openai.py             # OpenAI LLM Wrapper Helper
│   │   │      └── ollama.py             # Local Ollama CrewAI LLM Instantiation (qwen2.5:1.5b)
│   │   │
│   │   └── configs/
│   │          └── roles.json            # Agent Roles, Goals & Backstory Declarations
│   │
│   ├── repositories/                    # Data Access Layer
│   │      ├── interview_repository.py   # Pinecone Dense/Sparse Hybrid Search & Filtering
│   │      ├── session_repository.py     # MySQL Chat Sessions & Message History Repository
│   │      ├── evaluation_repository.py  # Evaluation Data Repository
│   │      └── role_repository.py        # Role Permissions Repository
│   │
│   ├── models/                          # Domain Data Models
│   │      ├── interview_question.py     # RAGState Flow Execution Model
│   │      ├── interview_session.py      # Session Domain Model
│   │      └── evaluation.py             # Evaluation Domain Model
│   │
│   ├── shared/                          # Utility & Helper Shared Layer
│   │      ├── exceptions/
│   │      │      └── custom_exceptions.py # Application & Domain Custom Exceptions
│   │      ├── utils/
│   │      │      ├── semantic_cache.py  # Vector Semantic Cache Lookup & Upsert Operations
│   │      │      ├── intent_utils.py    # Rule-Based Intent Detection & Query Normalizer
│   │      │      ├── history_utils.py   # Follow-Up Question Detector & Rewrite Wrapper
│   │      │      └── search_utils.py    # Hybrid Convex Scale Search Utilities
│   │      ├── validators/
│   │      │      └── question_validator.py# Length, Prompt Injection & SQL Injection Prevention
│   │      ├── helpers/
│   │      │      ├── reranker.py        # BAAI/bge-reranker-base CrossEncoder Reranking
│   │      │      └── context_builder.py # Context String & Metadata Source Map Constructor
│   │      └── response.py               # Standardized API Response Builders
│   │
│   ├── evaluation/                      # RAGAS Evaluation Framework
│   │      ├── evaluate_ragas.py         # RAGAS Pipeline Metric Evaluator Script
│   │      ├── test_dataset.json         # Evaluation Questions & Ground Truth Dataset
│   │      └── ragas_results_latest.csv  # Generated Metric Results Export
│   │
│   ├── config/
│   │      └── roles.json                # Global Role Configuration JSON
│   │
│   ├── tests/                           # Test Suite
│   │      ├── api/                      # Endpoint Integration Tests
│   │      ├── unit/                     # Business Logic Unit Tests
│   │      ├── integration/              # Pipeline End-to-End Tests
│   │      └── crew/                     # CrewAI Agent & Flow Tests
│   │
│   ├── logs/                            # Application Runtime Log Files
│   ├── bm25_values.json                 # Pre-computed Sparse BM25 Matrix Values
│   ├── .env                             # Environment Credentials Configuration
│   ├── requirements.txt                 # Python Dependencies Specifications
│   └── README.md                        # Backend Setup & Execution Guide
│
├── docs/                                # Technical Documentation
│   └── Architecture.md                  # Complete System Architectural Blueprint
│
└── frontend/                            # Angular Web Front-End Application
    ├── Dockerfile                       # Multi-stage Nginx Container Image Definition for Frontend
    ├── nginx.conf                       # Production Reverse Proxy Configuration
    ├── src/
    │   ├── app/
    │   │   ├── components/              # UI Components (Chat Widget, Auth, Admin, etc.)
    │   │   ├── services/                # HttpClient Service (chatbot.service.ts)
    │   │   ├── guards/                  # Angular Route Guards
    │   │   ├── models/                  # TypeScript Interfaces
    │   │   └── environments/            # Application Environment Variables
    ├── angular.json                     # Angular Build Configuration
    └── package.json                     # Node.js Dependency Specifications
```

---

## Architectural Highlights

### 1. High-Performance Modular Architecture
- **Single Responsibility Principle**: Every module in `backend/` handles a distinct concern (Routing, Schemas, Business Logic, Agent Engine, Vector Access, State Management, Utilities).
- **Fast Startup & Warm Cache**: Machine Learning models (`bge-small-en-v1.5`, `bge-reranker-base`, `BM25Encoder`) and Pinecone client instances are initialized as singletons in [`core/startup.py`](file:///d:/AI_Interview/xebia_document_search_platform/xebia_document_search_platform/backend/core/startup.py) to guarantee sub-millisecond setup latencies.

### 2. Multi-Stage Realtime RAG Flow Engine
1. **Sanitization & Security**: Input validation against SQL injection, script tags, and prompt injection attacks in [`shared/validators/question_validator.py`](file:///d:/AI_Interview/xebia_document_search_platform/xebia_document_search_platform/backend/shared/validators/question_validator.py).
2. **Deterministic Intent Detection**: Rule-based intent classifier for greetings and exits before incurring LLM overhead.
3. **Enterprise Taxonomy Classification**: CrewAI Agent classifies queries into domain-specific categories and intents.
4. **Conversational History Rewriting**: Contextual query transformation using MySQL conversation logs.
5. **Semantic Caching**: Pinecone vector cache lookup with configurable threshold (`0.90`) and automatic expiration.
6. **Hybrid Dense/Sparse Search**: Combined HuggingFace dense vector embeddings and BM25 sparse keyword scores with convex alpha scaling (`0.7`).
7. **Cross-Encoder Reranking**: Re-scores top retrieved documents using `BAAI/bge-reranker-base` to return high-precision context snippets.
8. **Context-Grounded Generation**: CrewAI Answer Agent strictly bound to retrieved context without hallucinations.

### 3. Automated Evaluation Suite
- Integrated [`evaluation/evaluate_ragas.py`](file:///d:/AI_Interview/xebia_document_search_platform/xebia_document_search_platform/backend/evaluation/evaluate_ragas.py) evaluating `context_precision`, `context_recall`, `faithfulness`, and `answer_relevancy` using local Ollama model instances and HuggingFace embeddings.

---

## Deployment & DevOps Architecture

### 4. Docker Compose Deployment
The entire platform can be spun up locally or in production environments with a single command using [`docker-compose.yml`](file:///d:/AI_Interview/xebia_document_search_platform/xebia_document_search_platform/docker-compose.yml):
```bash
docker compose up --build -d
```
**Orchestrated Services:**
- `mysql`: State-persisted MySQL 8.0 container holding chat sessions and messages.
- `ollama`: Ollama local LLM engine host.
- `backend`: FastAPI Python application container with automated healthcheck probe.
- `frontend`: Angular application built & served via Nginx reverse proxy routing API calls.

### 5. Kubernetes Production Deployment
The system includes enterprise-grade Kubernetes manifests under [`k8s/`](file:///d:/AI_Interview/xebia_document_search_platform/xebia_document_search_platform/k8s/):
- **ConfigMap & Secrets**: Managed in [`configmap.yaml`](file:///d:/AI_Interview/xebia_document_search_platform/xebia_document_search_platform/k8s/configmap.yaml) and [`secret.yaml`](file:///d:/AI_Interview/xebia_document_search_platform/xebia_document_search_platform/k8s/secret.yaml).
- **Auto-healing Deployments**: Scalable backend and frontend replica sets with readiness and liveness health probes in [`backend-deployment.yaml`](file:///d:/AI_Interview/xebia_document_search_platform/xebia_document_search_platform/k8s/backend-deployment.yaml) and [`frontend-deployment.yaml`](file:///d:/AI_Interview/xebia_document_search_platform/xebia_document_search_platform/k8s/frontend-deployment.yaml).
- **Ingress Controller**: Uniform external entry routing via [`ingress.yaml`](file:///d:/AI_Interview/xebia_document_search_platform/xebia_document_search_platform/k8s/ingress.yaml).

Apply manifests to cluster:
```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/ingress.yaml
```

### 6. CI/CD Automated Pipeline
Automated GitHub Actions pipeline defined in [`.github/workflows/ci-cd.yml`](file:///d:/AI_Interview/xebia_document_search_platform/xebia_document_search_platform/.github/workflows/ci-cd.yml):
- **Lint & Unit Tests**: Executes pytest suite on every push and pull request.
- **Build & Container Registry**: Builds production Docker images for backend and frontend and pushes them to Docker Hub.
- **Kubernetes CD Rollout**: Automatically deploys updated manifests and verifies successful rollout status.