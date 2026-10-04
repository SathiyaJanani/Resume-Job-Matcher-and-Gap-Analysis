"""
Seed script to populate all 12 tables with at least 12 high-quality, realistic records each.
Enterprise HR Tech / Resume Matching domain data.
"""

from datetime import datetime, timezone, timedelta
from backend.database import get_connection, init_db, TABLE_NAMES, get_table_counts

NOW = datetime.now(timezone.utc)


def dt(days_ago: int = 0) -> str:
    return (NOW - timedelta(days=days_ago)).isoformat()


def seed_database():
    init_db(force=True)

    with get_connection() as conn:
        cursor = conn.cursor()

        # -------------------------------------------------------------
        # 1. CANDIDATES (15 records)
        # -------------------------------------------------------------
        candidates = [
            ("Aravind Swaminathan", "aravind.s@example.com", "+91 98401 23456", "Chennai, India", "Senior ML Engineer", 6.5, "M.Tech in AI", "Active", dt(45)),
            ("Priya Sundaram", "priya.sundaram@example.com", "+91 98840 56789", "Bengaluru, India", "Full Stack Architect", 8.0, "B.E. Computer Science", "Active", dt(40)),
            ("Karthik Raman", "karthik.raman@example.com", "+91 94441 12345", "Hyderabad, India", "Cloud DevOps Lead", 7.0, "B.Tech Information Tech", "Interviewing", dt(38)),
            ("Deepa Venkatesh", "deepa.v@example.com", "+91 97900 98765", "Coimbatore, India", "NLP Research Scientist", 5.0, "Ph.D. Computational Linguistics", "Active", dt(35)),
            ("Siddharth Menon", "sid.menon@example.com", "+91 98450 11223", "Bengaluru, India", "Data Platform Engineer", 6.0, "M.S. Data Science", "Offered", dt(30)),
            ("Ananya Krishnan", "ananya.k@example.com", "+91 99620 44332", "Chennai, India", "Frontend UI/UX Specialist", 4.5, "B.Des & B.Tech", "Active", dt(28)),
            ("Vignesh Balaji", "vignesh.b@example.com", "+91 98412 88990", "Pune, India", "Backend Python Developer", 4.0, "B.E. Electronics & Comm", "Active", dt(25)),
            ("Sneha Nambiar", "sneha.n@example.com", "+91 97401 77665", "Kochi, India", "Computer Vision Specialist", 5.5, "M.Tech Robotics & AI", "Interviewing", dt(22)),
            ("Rahul Deshmukh", "rahul.d@example.com", "+91 98230 65432", "Mumbai, India", "Kubernetes & SRE Engineer", 6.0, "B.E. Information Tech", "Active", dt(20)),
            ("Meera Jayaraman", "meera.j@example.com", "+91 94432 55441", "Chennai, India", "AI Product Manager", 9.0, "MBA + B.E. CS", "Active", dt(18)),
            ("Gautam Ranganathan", "gautam.r@example.com", "+91 98845 33221", "Bengaluru, India", "Distributed Systems Engineer", 7.5, "M.S. Computer Science", "Screening", dt(15)),
            ("Divya Natarajan", "divya.n@example.com", "+91 99403 22110", "Hyderabad, India", "FastAPI / Microservices Lead", 5.0, "B.Tech CS", "Active", dt(12)),
            ("Sanjay Chandran", "sanjay.c@example.com", "+91 98409 66778", "Chennai, India", "Security & DevSecOps Engineer", 6.5, "M.Tech Cyber Security", "Active", dt(10)),
            ("Keerthana Prasad", "keerthana.p@example.com", "+91 97890 12398", "Bengaluru, India", "LLM Prompt & RAG Engineer", 3.5, "B.Tech AI & Data Science", "Offered", dt(7)),
            ("Harish Kumar", "harish.k@example.com", "+91 99625 77889", "Madurai, India", "Data Analyst & BI Specialist", 4.0, "B.Sc Computer Science & MCA", "Active", dt(4)),
        ]
        cursor.executemany("""
        INSERT INTO candidates (full_name, email, phone, location, current_title, years_experience, highest_degree, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, candidates)

        # -------------------------------------------------------------
        # 2. COMPANIES (14 records)
        # -------------------------------------------------------------
        companies = [
            ("Nexus AI Technologies", "Artificial Intelligence", "50-200", "Bengaluru, India", "https://nexusai.io", 4.8, 1, dt(60)),
            ("CloudMatrix Solutions", "Cloud & DevOps", "200-500", "Hyderabad, India", "https://cloudmatrix.com", 4.6, 1, dt(58)),
            ("Cognitive Pulse Labs", "Deep Tech & Healthcare AI", "20-50", "Chennai, India", "https://cognitivepulse.ai", 4.9, 1, dt(55)),
            ("FinTech Vertex", "Financial Technology", "500-1000", "Mumbai, India", "https://fintechvertex.com", 4.5, 1, dt(52)),
            ("Apex Data Systems", "Big Data & Analytics", "100-250", "Pune, India", "https://apexdatasys.com", 4.4, 1, dt(50)),
            ("HyperScale Networks", "SaaS & Infrastructure", "50-100", "Bengaluru, India", "https://hyperscalenet.io", 4.7, 1, dt(48)),
            ("Quantum Leap Robotics", "Robotics & Embedded AI", "20-50", "Coimbatore, India", "https://quantumleap.tech", 4.8, 1, dt(45)),
            ("Zenith HealthTech", "Health Sciences & MedTech", "100-200", "Chennai, India", "https://zenithhealth.org", 4.5, 1, dt(42)),
            ("Aegis Cyber Defense", "Cybersecurity", "200-500", "Bengaluru, India", "https://aegisdefense.com", 4.6, 1, dt(40)),
            ("Kavitham Digital Labs", "Enterprise Web & Mobile", "50-150", "Chennai, India", "https://kavithamlabs.com", 4.7, 1, dt(38)),
            ("Solvion Autonomous", "Autonomous Mobility", "50-100", "Hyderabad, India", "https://solvionauto.com", 4.7, 1, dt(35)),
            ("Orbital Logistics AI", "Supply Chain & Logistics", "100-300", "Mumbai, India", "https://orbitallogistics.ai", 4.4, 1, dt(30)),
            ("Synthetix NLP Studios", "Generative AI & LLMs", "10-50", "Bengaluru, India", "https://synthetixnlp.io", 4.9, 1, dt(25)),
            ("OmniRetail Engine", "E-commerce Tech", "250-500", "Gurugram, India", "https://omniretail.com", 4.3, 1, dt(20)),
        ]
        cursor.executemany("""
        INSERT INTO companies (name, industry, size_range, headquarters, website, rating, verified, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, companies)

        # -------------------------------------------------------------
        # 3. RECRUITERS (14 records)
        # -------------------------------------------------------------
        recruiters = [
            (1, "Rohan Verma", "rohan.v@nexusai.io", "Principal Talent Partner", "AI/ML Talent", 5, "+91 98401 10001", dt(55)),
            (1, "Lavanya Rao", "lavanya.r@nexusai.io", "Technical Recruiter", "Engineering Talent", 4, "+91 98401 10002", dt(50)),
            (2, "Manish Sharma", "m.sharma@cloudmatrix.com", "Head of Talent Acquisition", "Cloud & Infra", 6, "+91 98401 10003", dt(52)),
            (3, "Dr. Sangeetha Nair", "sangeetha@cognitivepulse.ai", "Talent Director", "R&D Hiring", 3, "+91 98401 10004", dt(48)),
            (4, "Aditya Kulkarni", "aditya.k@fintechvertex.com", "Senior HR Business Partner", "Fintech Products", 8, "+91 98401 10005", dt(46)),
            (5, "Nithya Subramanian", "nithya@apexdatasys.com", "Lead Technical Recruiter", "Data Engineering", 4, "+91 98401 10006", dt(44)),
            (6, "Varun Kapoor", "varun.k@hyperscalenet.io", "Talent Sourcing Specialist", "SaaS Engineering", 3, "+91 98401 10007", dt(42)),
            (7, "Pooja Hegde", "pooja.h@quantumleap.tech", "HR Manager", "Robotics & Hardware", 2, "+91 98401 10008", dt(39)),
            (8, "Kishore Kumar", "kishore@zenithhealth.org", "Senior Recruiter", "Clinical & Tech", 4, "+91 98401 10009", dt(35)),
            (9, "Shreya Joshi", "shreya.j@aegisdefense.com", "Cyber Talent Scout", "Information Security", 5, "+91 98401 10010", dt(32)),
            (10, "Suresh Raghavan", "suresh.r@kavithamlabs.com", "Director of People Ops", "Full Stack & Design", 6, "+91 98401 10011", dt(28)),
            (11, "Tarun Reddy", "tarun.r@solvionauto.com", "Talent Acquisition Lead", "Autonomous Tech", 3, "+91 98401 10012", dt(25)),
            (12, "Preeti Saxena", "preeti.s@orbitallogistics.ai", "Recruiter", "Supply Chain Analytics", 4, "+91 98401 10013", dt(20)),
            (13, "Ashwin Parthasarathy", "ashwin@synthetixnlp.io", "Founding Talent Lead", "GenAI & LLM", 5, "+91 98401 10014", dt(15)),
        ]
        cursor.executemany("""
        INSERT INTO recruiters (company_id, full_name, email, role, department, active_requisitions, phone, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, recruiters)

        # -------------------------------------------------------------
        # 4. JOBS (15 records)
        # -------------------------------------------------------------
        jobs = [
            (1, 1, "Lead Machine Learning Engineer", "AI Research", "Full-time", "Senior (5-8 yrs)", "Hybrid (Bengaluru)", "₹32L - ₹48L", "Architect and deploy production LLM pipelines, PyTorch models, and real-time inference microservices.", "Open", dt(40)),
            (1, 2, "Senior NLP / GenAI Specialist", "AI Research", "Full-time", "Mid-Senior (4-7 yrs)", "Remote", "₹28L - ₹42L", "Design RAG workflows, vector index search, and fine-tune transformer models using HuggingFace & vLLM.", "Open", dt(38)),
            (2, 3, "Principal Cloud DevOps Architect", "Cloud Engineering", "Full-time", "Lead (7-10 yrs)", "On-site (Hyderabad)", "₹35L - ₹55L", "Orchestrate multi-region Kubernetes clusters on AWS/GCP, Terraform IaC, and zero-trust security pipelines.", "Open", dt(36)),
            (3, 4, "Computer Vision Scientist", "BioTech AI", "Full-time", "Senior (4-8 yrs)", "Hybrid (Chennai)", "₹26L - ₹38L", "Build 3D biomedical image segmentation algorithms with PyTorch, OpenCV, and TensorRT acceleration.", "Open", dt(33)),
            (4, 5, "Staff Backend Engineer (Python/FastAPI)", "Payments Core", "Full-time", "Senior (6-9 yrs)", "Hybrid (Mumbai)", "₹30L - ₹45L", "Scale high-throughput transaction engines handling 50k requests/sec using FastAPI, Redis, and PostgreSQL.", "Open", dt(30)),
            (5, 6, "Senior Data Platform Engineer", "Data Platform", "Full-time", "Mid-Senior (5-8 yrs)", "Remote", "₹26L - ₹38L", "Design real-time Spark/Flink streaming pipelines, Delta Lake storage, and Snowflake data warehouses.", "Open", dt(28)),
            (6, 7, "Frontend Design Systems Lead", "Product Experience", "Full-time", "Lead (6-9 yrs)", "Remote", "₹25L - ₹36L", "Craft pixel-perfect micro-interactions, responsive dashboard interfaces, and accessible design system components.", "Open", dt(25)),
            (7, 8, "Embedded AI / ROS Engineer", "Robotics", "Full-time", "Mid-Senior (3-6 yrs)", "On-site (Coimbatore)", "₹20L - ₹30L", "Develop edge AI inference on NVIDIA Jetson using C++, ROS2, and ONNX Runtime for autonomous mobile robots.", "Open", dt(22)),
            (8, 9, "Clinical Data Analyst", "Health Informatics", "Full-time", "Mid (3-5 yrs)", "Hybrid (Chennai)", "₹14L - ₹22L", "Extract actionable clinical metrics from EHR databases, perform statistical analyses, and build Tableau dashboards.", "Open", dt(20)),
            (9, 10, "DevSecOps & Cloud Security Specialist", "Security", "Full-time", "Senior (5-8 yrs)", "Remote", "₹28L - ₹40L", "Implement container security scanning, IAM policies, SAST/DAST, and SOC2 compliance across AWS infrastructure.", "Open", dt(18)),
            (10, 11, "Full Stack Engineering Manager", "Web Applications", "Full-time", "Manager (8-12 yrs)", "Hybrid (Chennai)", "₹38L - ₹52L", "Lead a team of 10 engineers building SaaS analytics portals with modern React, Node.js, and Python backend.", "Open", dt(15)),
            (11, 12, "Sensor Fusion & SLAM Engineer", "Perception", "Full-time", "Senior (4-7 yrs)", "On-site (Hyderabad)", "₹25L - ₹38L", "Develop multi-sensor calibration, LiDAR-camera fusion, and state estimation algorithms in C++.", "Open", dt(12)),
            (12, 13, "Predictive Logistics Data Scientist", "Supply Chain", "Full-time", "Mid-Senior (4-7 yrs)", "Hybrid (Mumbai)", "₹22L - ₹34L", "Develop demand forecasting time-series models, route optimization algorithms, and inventory simulation tools.", "Open", dt(10)),
            (13, 14, "LLM Evaluation & Alignment Researcher", "Foundation Models", "Full-time", "Research (3-6 yrs)", "Remote", "₹32L - ₹50L", "Benchmark hallucination rates, RLHF/DPO alignments, and synthesize synthetic training datasets.", "Open", dt(7)),
            (14, 11, "E-commerce Search & Recommendation Engineer", "Discovery", "Full-time", "Senior (5-8 yrs)", "Hybrid (Gurugram)", "₹28L - ₹42L", "Build vector search, hybrid Elasticsearch ranking, and real-time personalized product recommendations.", "Open", dt(4)),
        ]
        cursor.executemany("""
        INSERT INTO jobs (company_id, recruiter_id, title, department, employment_type, experience_level, location_type, salary_range, description, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, jobs)

        # -------------------------------------------------------------
        # 5. SKILLS (20 records)
        # -------------------------------------------------------------
        skills = [
            ("Python", "Programming Language", 98, "High", dt(90)),
            ("PyTorch", "AI / Deep Learning", 96, "High", dt(90)),
            ("Transformers & HuggingFace", "Generative AI", 95, "Very High", dt(90)),
            ("FastAPI", "Backend Framework", 92, "High", dt(90)),
            ("Docker & Containerization", "DevOps & Cloud", 90, "High", dt(90)),
            ("Kubernetes (K8s)", "DevOps & Cloud", 94, "Very High", dt(90)),
            ("AWS Cloud Architecture", "Cloud Platforms", 93, "High", dt(90)),
            ("PostgreSQL & SQL", "Databases", 91, "High", dt(90)),
            ("Natural Language Processing (NLP)", "AI / Machine Learning", 92, "High", dt(90)),
            ("Vector Databases (Pinecone/Chroma/Qdrant)", "Generative AI", 94, "Very High", dt(90)),
            ("LangChain & LlamaIndex", "Generative AI", 89, "High", dt(90)),
            ("Apache Spark & Big Data", "Data Engineering", 86, "Moderate", dt(90)),
            ("React.js & Modern Frontend", "Frontend", 88, "High", dt(90)),
            ("TypeScript", "Frontend & Fullstack", 90, "High", dt(90)),
            ("Computer Vision & OpenCV", "AI / Machine Learning", 85, "Moderate", dt(90)),
            ("CI/CD (GitHub Actions/GitLab)", "DevOps & Cloud", 87, "Moderate", dt(90)),
            ("Terraform & IaC", "DevOps & Cloud", 88, "High", dt(90)),
            ("C++ Systems Programming", "Systems & Embedded", 82, "Moderate", dt(90)),
            ("MLOps (MLflow/WandB)", "AI / Machine Learning", 90, "High", dt(90)),
            ("System Design & Microservices", "Architecture", 95, "Very High", dt(90)),
        ]
        cursor.executemany("""
        INSERT INTO skills (skill_name, category, demand_score, popularity_level, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, skills)

        # -------------------------------------------------------------
        # 6. CANDIDATE_SKILLS (25 records)
        # -------------------------------------------------------------
        candidate_skills = [
            # Candidate 1: Aravind (Senior ML Engineer)
            (1, 1, "Expert", 6.5, 1, dt(45)),   # Python
            (1, 2, "Expert", 5.5, 1, dt(45)),   # PyTorch
            (1, 3, "Advanced", 4.0, 1, dt(45)), # Transformers
            (1, 19, "Advanced", 4.0, 1, dt(45)),# MLOps
            # Candidate 2: Priya (Full Stack Architect)
            (2, 1, "Expert", 8.0, 1, dt(40)),   # Python
            (2, 4, "Expert", 6.0, 1, dt(40)),   # FastAPI
            (2, 8, "Expert", 8.0, 1, dt(40)),   # PostgreSQL
            (2, 13, "Advanced", 5.0, 1, dt(40)),# React
            # Candidate 3: Karthik (Cloud DevOps Lead)
            (3, 5, "Expert", 7.0, 1, dt(38)),   # Docker
            (3, 6, "Expert", 6.5, 1, dt(38)),   # K8s
            (3, 7, "Expert", 7.0, 1, dt(38)),   # AWS
            (3, 17, "Expert", 5.5, 1, dt(38)),  # Terraform
            # Candidate 4: Deepa (NLP Research Scientist)
            (4, 1, "Expert", 5.0, 1, dt(35)),   # Python
            (4, 9, "Expert", 5.0, 1, dt(35)),   # NLP
            (4, 3, "Expert", 4.5, 1, dt(35)),   # Transformers
            (4, 10, "Advanced", 3.0, 1, dt(35)),# Vector DBs
            # Candidate 5: Siddharth (Data Platform Engineer)
            (5, 1, "Advanced", 6.0, 1, dt(30)), # Python
            (5, 12, "Expert", 5.0, 1, dt(30)),  # Spark
            (5, 8, "Advanced", 6.0, 1, dt(30)), # SQL
            # Candidate 6: Ananya (Frontend UI/UX)
            (6, 13, "Expert", 4.5, 1, dt(28)),  # React
            (6, 14, "Expert", 4.0, 1, dt(28)),  # TypeScript
            # Candidate 7: Keerthana (LLM Prompt & RAG)
            (14, 1, "Advanced", 3.5, 1, dt(7)), # Python
            (14, 3, "Expert", 3.0, 1, dt(7)),   # Transformers
            (14, 10, "Expert", 2.5, 1, dt(7)),  # Vector DBs
            (14, 11, "Expert", 2.5, 1, dt(7)),  # LangChain
        ]
        cursor.executemany("""
        INSERT INTO candidate_skills (candidate_id, skill_id, proficiency_level, years_experience, verified, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, candidate_skills)

        # -------------------------------------------------------------
        # 7. JOB_SKILLS (25 records)
        # -------------------------------------------------------------
        job_skills = [
            # Job 1: Lead ML Engineer
            (1, 1, 1, 1.0, 5.0, dt(40)),  # Python (Req)
            (1, 2, 1, 1.0, 4.0, dt(40)),  # PyTorch (Req)
            (1, 3, 1, 0.9, 3.0, dt(40)),  # Transformers (Req)
            (1, 19, 0, 0.8, 2.0, dt(40)), # MLOps (Pref)
            # Job 2: Senior NLP / GenAI
            (2, 1, 1, 1.0, 4.0, dt(38)),  # Python (Req)
            (2, 3, 1, 1.0, 3.0, dt(38)),  # Transformers (Req)
            (2, 9, 1, 0.9, 4.0, dt(38)),  # NLP (Req)
            (2, 10, 1, 0.8, 2.0, dt(38)), # Vector DBs (Req)
            # Job 3: Principal Cloud DevOps
            (3, 5, 1, 1.0, 5.0, dt(36)),  # Docker (Req)
            (3, 6, 1, 1.0, 5.0, dt(36)),  # K8s (Req)
            (3, 7, 1, 1.0, 6.0, dt(36)),  # AWS (Req)
            (3, 17, 1, 0.9, 4.0, dt(36)), # Terraform (Req)
            # Job 4: Computer Vision Scientist
            (4, 1, 1, 1.0, 4.0, dt(33)),  # Python (Req)
            (4, 2, 1, 1.0, 4.0, dt(33)),  # PyTorch (Req)
            (4, 15, 1, 1.0, 3.0, dt(33)), # Computer Vision (Req)
            # Job 5: Staff Backend Engineer
            (5, 1, 1, 1.0, 5.0, dt(30)),  # Python (Req)
            (5, 4, 1, 1.0, 4.0, dt(30)),  # FastAPI (Req)
            (5, 8, 1, 1.0, 5.0, dt(30)),  # SQL (Req)
            (5, 20, 1, 0.9, 4.0, dt(30)), # System Design (Req)
            # Job 6: Senior Data Platform Engineer
            (6, 1, 1, 1.0, 4.0, dt(28)),  # Python (Req)
            (6, 12, 1, 1.0, 4.0, dt(28)), # Spark (Req)
            (6, 8, 1, 0.9, 4.0, dt(28)),  # SQL (Req)
            # Job 7: Frontend Design Systems
            (7, 13, 1, 1.0, 5.0, dt(25)), # React (Req)
            (7, 14, 1, 1.0, 4.0, dt(25)), # TypeScript (Req)
        ]
        cursor.executemany("""
        INSERT INTO job_skills (job_id, skill_id, is_required, importance_weight, min_years, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, job_skills)

        # -------------------------------------------------------------
        # 8. RESUMES (15 records)
        # -------------------------------------------------------------
        resumes = [
            (1, "aravind_swaminathan_ai_lead.pdf", 245, "Experienced Senior ML Engineer with 6.5+ years building deep learning systems, PyTorch neural nets, transformer based RAG models, and deploying low-latency FastAPI endpoints on Kubernetes.", "Senior Machine Learning specialist with deep NLP & PyTorch architecture expertise.", "Senior", dt(45)),
            (2, "priya_sundaram_fullstack_lead.pdf", 312, "Full Stack Architect specializing in high-performance web systems, FastAPI backends, PostgreSQL schemas, and modern React TypeScript component libraries.", "Accomplished architect with 8 years scaling web services and microservices.", "Lead", dt(40)),
            (3, "karthik_raman_cloud_devops.pdf", 198, "DevOps Engineer with 7 years hands-on production experience with multi-cloud AWS architectures, Kubernetes cluster scaling, Terraform modules, and CI/CD pipelines.", "Cloud infrastructure expert with extensive SRE, K8s, and Terraform capability.", "Lead", dt(38)),
            (4, "deepa_venkatesh_nlp_phd.pdf", 410, "NLP Research Scientist with Ph.D. in Computational Linguistics. 5 years applied experience with HuggingFace transformers, cross-attention architectures, BERT, and semantic search vectors.", "Advanced NLP Researcher with proven record in generative AI & retrieval systems.", "Senior", dt(35)),
            (5, "siddharth_menon_data_platform.pdf", 260, "Data Platform Engineer with 6 years experience in Apache Spark, Kafka streaming pipelines, Delta Lake storage, Snowflake schemas, and Python automation.", "Big Data infrastructure specialist handling terabyte-scale distributed ingestion.", "Senior", dt(30)),
            (6, "ananya_krishnan_uiux_frontend.pdf", 215, "Frontend Design Systems Specialist with 4.5 years experience in React, TypeScript, responsive CSS architectures, Webpack/Vite, and WCAG accessibility standards.", "Creative and detail-oriented frontend engineer building modern interactive web apps.", "Mid-Senior", dt(28)),
            (7, "vignesh_balaji_backend_python.pdf", 185, "Backend Developer with 4 years building async Python APIs, FastAPI services, SQLAlchemy ORM, Redis caching layers, and Docker container packaging.", "Skilled Python backend developer with strong database & REST API expertise.", "Mid-Level", dt(25)),
            (8, "sneha_nambiar_computervision.pdf", 295, "Computer Vision Engineer with 5.5 years in PyTorch, OpenCV, TensorRT, object detection models (YOLO), and automated visual inspection systems.", "Specialist in real-time embedded vision and convolutional neural networks.", "Senior", dt(22)),
            (9, "rahul_deshmukh_sre_k8s.pdf", 220, "SRE & Kubernetes Engineer with 6 years maintaining 99.99% uptime, Prometheus/Grafana monitoring, Helm charts, and incident response automation.", "DevOps and reliability engineer with deep container orchestration knowledge.", "Senior", dt(20)),
            (10, "meera_jayaraman_ai_pm.pdf", 340, "AI Product Manager with 9 years bridging deep technical machine learning capabilities with business roadmaps, user research, and executive alignment.", "Product leader delivering enterprise AI and automated decision products.", "Principal", dt(18)),
            (11, "gautam_ranganathan_systems.pdf", 275, "Distributed Systems Engineer with 7.5 years building low-latency gRPC services, fault-tolerant message queues, consensus protocols, and scalable microservices.", "High-throughput systems expert with deep systems design mastery.", "Lead", dt(15)),
            (12, "divya_natarajan_fastapi_micro.pdf", 205, "Microservices Developer with 5 years experience designing resilient REST and event-driven architectures with Python FastAPI, Celery, and PostgreSQL.", "API specialist with strong async programming and schema modeling proficiency.", "Senior", dt(12)),
            (13, "sanjay_chandran_secops.pdf", 230, "DevSecOps Specialist with 6.5 years implementing automated vulnerability scanning, cloud IAM audits, SAST/DAST pipelines, and SOC2 compliance.", "Security engineer embedding protective safeguards into modern CI/CD lifecycles.", "Senior", dt(10)),
            (14, "keerthana_prasad_rag_llm.pdf", 190, "LLM Application Engineer with 3.5 years building production RAG pipelines with LangChain, LlamaIndex, ChromaDB vector stores, and prompt evaluation benchmarks.", "Generative AI engineer adept at prompt engineering, embeddings, and vector databases.", "Mid-Level", dt(7)),
            (15, "harish_kumar_bi_analytics.pdf", 175, "Data Analyst with 4 years creating interactive executive dashboards in Power BI and Tableau, writing advanced SQL queries, and predictive modeling.", "Business intelligence professional skilled at exploratory data analysis.", "Mid-Level", dt(4)),
        ]
        cursor.executemany("""
        INSERT INTO resumes (candidate_id, file_name, file_size_kb, raw_text, parsed_summary, ai_detected_seniority, uploaded_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, resumes)

        # -------------------------------------------------------------
        # 9. JOB_APPLICATIONS (16 records)
        # -------------------------------------------------------------
        applications = [
            (1, 1, 1, "Technical Interview", dt(25), "Active", "Strong technical match on PyTorch & FastAPI. Cleared initial screening with top marks."),
            (1, 2, 2, "Offer", dt(20), "Offered", "Exceptional score on RAG design and domain architecture."),
            (2, 5, 5, "Applied", dt(18), "Under Review", "Applied through referral. Resume matches required microservices stack."),
            (2, 7, 7, "Culture Fit", dt(15), "Interviewing", "Demonstrated exceptional team leadership and UI architecture experience."),
            (3, 3, 3, "Technical Interview", dt(14), "Interviewing", "Live cluster configuration test scheduled for Thursday."),
            (4, 2, 2, "Technical Interview", dt(12), "Interviewing", "Deep theoretical knowledge of attention mechanisms and HuggingFace fine-tuning."),
            (4, 4, 4, "Applied", dt(10), "Under Review", "Profile submitted for biomedical AI scientist opening."),
            (5, 6, 6, "Offer", dt(9), "Offered", "Offer letter extended for Senior Data Platform role. Acceptance pending."),
            (6, 7, 7, "Screening", dt(8), "Screening", "Recruiter phone call scheduled to discuss design system philosophy."),
            (7, 5, 5, "Applied", dt(7), "Under Review", "Standard web application submitted via portal."),
            (8, 4, 4, "Technical Interview", dt(6), "Interviewing", "Practical coding challenge on TensorRT optimization submitted."),
            (9, 3, 3, "Screening", dt(5), "Screening", "Phone screen passed. Moving to technical round."),
            (10, 11, 11, "Culture Fit", dt(4), "Interviewing", "Interview with Head of Engineering on product vision."),
            (11, 15, 11, "Screening", dt(3), "Screening", "Search system background closely aligns with job description."),
            (14, 2, 2, "Offer", dt(2), "Offered", "Outstanding performance on RAG evaluation challenge."),
            (15, 9, 9, "Applied", dt(1), "Under Review", "Application received for Clinical Data Analyst."),
        ]
        cursor.executemany("""
        INSERT INTO job_applications (candidate_id, job_id, recruiter_id, stage, applied_date, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, applications)

        # -------------------------------------------------------------
        # 10. MATCH_RESULTS (15 records)
        # -------------------------------------------------------------
        matches = [
            (1, 1, 94.5, 96.0, 92.0, 95.0, "Python, PyTorch, Transformers, MLOps, System Design", "Kubernetes advanced scaling", "Excellent candidate with exact match for Lead ML requirements. High semantic and skill alignment.", dt(20)),
            (1, 2, 91.2, 93.5, 88.0, 90.0, "Python, Transformers, NLP, Vector DBs", "LangChain enterprise workflows", "Strong NLP expertise and direct hands-on transformer experience.", dt(19)),
            (2, 5, 92.8, 94.0, 91.5, 93.0, "Python, FastAPI, SQL, PostgreSQL, System Design", "Redis cluster caching", "Great match for Staff Backend Engineer. Clear leadership and architectural depth.", dt(18)),
            (2, 7, 85.0, 87.0, 82.0, 86.0, "React, TypeScript, System Design", "Design system tokens, Figma sync", "Solid frontend match with architectural capabilities.", dt(17)),
            (3, 3, 96.5, 97.0, 95.5, 98.0, "Docker, K8s, AWS, Terraform, CI/CD", "Advanced FinOps optimization", "Perfect candidate profile for Cloud DevOps Architect requisition.", dt(16)),
            (4, 2, 95.0, 98.0, 92.0, 96.0, "Python, NLP, Transformers, PyTorch", "FastAPI production serving", "Premier academic and research candidate in computational linguistics.", dt(15)),
            (4, 4, 82.5, 84.0, 80.0, 81.0, "Python, PyTorch", "OpenCV 3D Medical imaging", "Candidate has deep theoretical skills; needs minor upskilling in medical image formats.", dt(14)),
            (5, 6, 93.5, 95.0, 91.0, 94.0, "Python, Spark, SQL, Big Data", "Snowflake streaming connectors", "High proficiency in distributed data processing frameworks.", dt(13)),
            (6, 7, 91.0, 93.0, 89.0, 90.0, "React, TypeScript, CSS, UI/UX", "Micro-frontends orchestration", "Exceptional visual sensitivity and strong modern UI engineering background.", dt(12)),
            (7, 5, 84.0, 86.0, 81.0, 83.0, "Python, FastAPI, SQL", "Distributed systems high-concurrency", "Capable backend engineer with room to grow into staff-level scaling.", dt(10)),
            (8, 4, 94.0, 95.5, 92.5, 93.5, "Python, PyTorch, Computer Vision, OpenCV", "TensorRT embedded deployment", "Strong match for autonomous vision and camera perception.", dt(8)),
            (9, 3, 90.5, 92.0, 88.5, 89.5, "Docker, K8s, AWS, CI/CD", "Terraform module composition", "Proven SRE practices with high uptime track record.", dt(6)),
            (10, 11, 88.0, 90.0, 85.0, 87.0, "System Design, Microservices, Agile", "Hands-on React coding", "Outstanding product delivery leader with strong tech background.", dt(4)),
            (14, 2, 93.0, 95.0, 91.0, 92.0, "Python, Transformers, Vector DBs, LangChain", "Multi-GPU inference cluster tuning", "High-potential talent for generative AI application layer and retrieval.", dt(2)),
            (15, 9, 86.5, 88.0, 84.0, 85.0, "SQL, BI Analytics, Python", "Clinical terminology SNOMED CT", "Solid data analytics professional ready for healthcare reporting.", dt(1)),
        ]
        cursor.executemany("""
        INSERT INTO match_results (candidate_id, job_id, match_score, semantic_similarity, skill_overlap_score, readiness_percentage, matched_skills, missing_skills, ai_summary, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, matches)

        # -------------------------------------------------------------
        # 11. INTERVIEWS (14 records)
        # -------------------------------------------------------------
        interviews = [
            (1, 1, "Technical System Design", dt(-2), 60, "https://meet.google.com/abc-defg-hij", "Candidate showed masterful command of distributed model training and latency budgets.", 9.5, "Scheduled", dt(5)),
            (2, 2, "Leadership & Culture", dt(-1), 45, "https://meet.google.com/xyz-uvwx-rst", "Strong communication and clear empathy. High ownership mentality.", 9.2, "Scheduled", dt(4)),
            (3, 5, "Coding & Data Structures", dt(-3), 60, "https://meet.google.com/lmn-opqr-stu", "Solved graph optimization problem within 25 minutes with optimal O(N) complexity.", 8.8, "Scheduled", dt(3)),
            (4, 7, "Architecture Review", dt(-4), 75, "https://meet.google.com/jkl-mnop-qrs", "Walked through micro-frontend decoupled state management cleanly.", 8.5, "Scheduled", dt(2)),
            (5, 3, "Cloud Infrastructure Deep Dive", dt(-2), 60, "https://meet.google.com/tuv-wxyz-abc", "Demonstrated automated Terraform rollout with canary ingress.", 9.4, "Scheduled", dt(2)),
            (6, 2, "NLP Research Presentation", dt(1), 60, "https://meet.google.com/def-ghij-klm", "Presented novel findings on few-shot prompt compression.", 9.6, "Completed", dt(3)),
            (7, 4, "Initial Recruiter Screen", dt(2), 30, "https://meet.google.com/nop-qrst-uvw", "Candidate explained career transition from linguistics to applied AI clearly.", 8.0, "Completed", dt(4)),
            (8, 6, "Big Data Hands-on Challenge", dt(3), 90, "https://meet.google.com/zab-cdef-ghi", "Built resilient PySpark streaming pipeline with checkpointing.", 9.0, "Completed", dt(5)),
            (9, 7, "Portfolio & Component Design", dt(4), 45, "https://meet.google.com/jkl-uvwx-yza", "Showcased high-grade micro-animations and accessibility adherence.", 8.9, "Completed", dt(6)),
            (10, 5, "Backend API Design Round", dt(5), 60, "https://meet.google.com/bcd-efgh-ijk", "Clean FastAPI schema definitions and database connection pooling.", 8.2, "Completed", dt(7)),
            (11, 4, "Computer Vision Model Optimization", dt(6), 60, "https://meet.google.com/lmn-opqr-zab", "Walked through quantization techniques and ONNX inference engine.", 9.3, "Completed", dt(8)),
            (12, 3, "Site Reliability Case Study", dt(7), 60, "https://meet.google.com/cde-fghi-jkl", "Handled simulated multi-region DNS failover smoothly.", 8.7, "Completed", dt(9)),
            (13, 11, "Executive Management Round", dt(8), 45, "https://meet.google.com/mno-pqrs-tuv", "Articulated talent retention strategies and engineering sprint cadences.", 9.1, "Completed", dt(10)),
            (14, 2, "Generative AI Systems Challenge", dt(9), 75, "https://meet.google.com/wxy-zabc-def", "Live-coded vector reranking pipeline with cross-encoder scoring.", 9.7, "Completed", dt(11)),
        ]
        cursor.executemany("""
        INSERT INTO interviews (application_id, recruiter_id, round_name, scheduled_at, duration_minutes, meeting_link, interviewer_notes, rating_score, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, interviews)

        # -------------------------------------------------------------
        # 12. LEARNING_RECOMMENDATIONS (15 records)
        # -------------------------------------------------------------
        learning_recs = [
            (1, 6, "Production Kubernetes for ML Engineers", "Coursera / DeepLearning.AI", "https://coursera.org/learn/k8s-mlops", 24, "Advanced", "High", "In Progress", dt(10)),
            (1, 10, "Vector Databases at Scale with Pinecone & Milvus", "DeepLearning.AI", "https://deeplearning.ai/short-courses/vector-db", 12, "Intermediate", "Medium", "Recommended", dt(12)),
            (2, 20, "Enterprise Microservices Design & Resiliency", "Udemy", "https://udemy.com/course/microservices-architecture", 30, "Advanced", "High", "Completed", dt(15)),
            (3, 17, "Advanced Terraform Cloud Infrastructure Automation", "HashiCorp Learn", "https://developer.hashicorp.com/terraform/tutorials", 20, "Advanced", "High", "In Progress", dt(14)),
            (4, 4, "FastAPI Microservices for Deep Learning Models", "TestDriven.io", "https://testdriven.io/courses/fastapi-celery", 18, "Intermediate", "Medium", "Recommended", dt(13)),
            (5, 10, "Vector Search Systems & Hybrid Information Retrieval", "edX", "https://edx.org/course/vector-search", 25, "Advanced", "Medium", "Recommended", dt(11)),
            (6, 14, "Advanced TypeScript Design Patterns & Generics", "Frontend Masters", "https://frontendmasters.com/courses/typescript", 16, "Advanced", "High", "Completed", dt(9)),
            (7, 20, "High-Throughput Distributed Systems with Python", "Real Python", "https://realpython.com/distributed-systems", 22, "Advanced", "High", "In Progress", dt(8)),
            (8, 2, "TensorRT Optimization for Real-Time Inference", "NVIDIA Deep Learning Institute", "https://courses.nvidia.com/courses/tensorrt", 15, "Advanced", "High", "Completed", dt(7)),
            (9, 6, "Certified Kubernetes Administrator (CKA) Path", "Linux Foundation", "https://training.linuxfoundation.org/cka", 40, "Expert", "High", "In Progress", dt(6)),
            (10, 11, "Designing AI-Powered User Experiences", "Interaction Design Foundation", "https://interaction-design.org/courses/ai-ux", 18, "Intermediate", "Medium", "Completed", dt(5)),
            (11, 20, "Consensus Algorithms: Paxos, Raft, and Gossip Protocols", "MIT OpenCourseWare", "https://ocw.mit.edu/courses/distributed-systems", 35, "Expert", "High", "Recommended", dt(4)),
            (12, 8, "Advanced PostgreSQL Indexing and Performance Tuning", "Postgres University", "https://pganalyze.com/academy", 14, "Advanced", "Medium", "Recommended", dt(3)),
            (14, 3, "Fine-Tuning Open Source LLMs with LoRA & QLoRA", "HuggingFace Deep Learning", "https://huggingface.co/learn/deep-rl", 16, "Advanced", "High", "In Progress", dt(2)),
            (15, 1, "Python for Data Analysis and Predictive Modeling", "DataCamp", "https://datacamp.com/tracks/data-analyst", 28, "Intermediate", "High", "In Progress", dt(1)),
        ]
        cursor.executemany("""
        INSERT INTO learning_recommendations (candidate_id, skill_id, course_title, platform, url, estimated_hours, difficulty_level, priority, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, learning_recs)

        conn.commit()

    print("Successfully seeded all 12 tables.")
    counts = get_table_counts()
    for name, count in counts.items():
        print(f"Table '{name}': {count} records")


if __name__ == "__main__":
    seed_database()
