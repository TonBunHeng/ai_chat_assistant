import re
import json
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.services.intent_service import intent_service
from app.services.online.gemini_service import gemini_online_service

class SuggestionService:
    """
    Intelligent Context-Aware Suggestion Generator for Cambodia Super AI.
    Generates dynamic, relevant follow-up topics following conversation flow:
    - Tourism & Travel stages (Itinerary, Angkor Wat, transport, budget)
    - Business & Economy stages (Starting business, CamDX registration, tax, Bakong)
    - Programming & AI stages (Architecture, LLM API, history, RAG, vector DBs)
    - Government & Public Services (Passports, Visas, Driver licenses, Sangkat OWSO)
    - Education & Research (BacII exams, universities, STEM)
    - Khmer Language & Translation (Formal letters, Chuon Nath orthography)
    - Mathematics & Science (Gradient descent, algorithms, calculus)
    """

    def generate_context_suggestions(
        self,
        message: str,
        answer: str = "",
        conversation_history: Optional[List[Dict[str, str]]] = None,
        language: str = "en",
        intent: Optional[str] = None,
        rag_sources: Optional[List[Dict[str, Any]]] = None,
        exclude: Optional[List[str]] = None,
        refresh: bool = False,
        history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Generate 4 concise, actionable, non-duplicative follow-up suggestions
        tailored to the ongoing dialogue and recent AI response.
        """
        user_msg = (message or "").strip()
        ai_ans = (answer or "").strip()
        hist = conversation_history or history or []
        excl = set(exclude or [])

        # Detect effective language
        is_km = (
            language == "km" or
            bool(re.search(r'[\u1780-\u17FF]', user_msg)) or
            bool(re.search(r'[\u1780-\u17FF]', ai_ans[:100]))
        )
        lang_code = "km" if is_km else "en"

        # Detect or refine intent & conversation stage
        if not intent or intent == "general_qa":
            det = intent_service.detect_intent(user_msg, hist)
            intent = det.get("intent", "general_qa")

        # 1. Try Gemini Online for real-time dynamic semantic follow-ups if available
        if gemini_online_service.is_available() and len(user_msg) > 3:
            try:
                ai_suggestions = self._generate_with_gemini(
                    user_msg=user_msg,
                    ai_ans=ai_ans,
                    history=hist,
                    intent=intent,
                    lang_code=lang_code,
                    exclude=excl,
                    refresh=refresh
                )
                if ai_suggestions and len(ai_suggestions.get("suggestions", [])) >= 4:
                    return {
                        "topic": ai_suggestions.get("topic", "Contextual Follow-ups"),
                        "suggestions": ai_suggestions["suggestions"][:4]
                    }
            except Exception as e:
                # Fast fallback to deterministic rule synthesizer
                pass

        # 2. Rule Synthesizer: High-accuracy domain context state machine
        fallback_res = self._synthesize_contextual_suggestions(
            user_msg=user_msg,
            ai_ans=ai_ans,
            intent=intent,
            lang_code=lang_code,
            exclude=excl,
            refresh=refresh
        )
        return fallback_res

    def _generate_with_gemini(
        self,
        user_msg: str,
        ai_ans: str,
        history: List[Dict[str, str]],
        intent: str,
        lang_code: str,
        exclude: set,
        refresh: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Query Gemini with a strict schema to generate 4 follow-up suggestions."""
        prompt = (
            f"You are the Suggestion Engine for Cambodia Super AI.\n"
            f"Given the conversation state below, generate exactly 4 concise, context-aware follow-up question suggestions "
            f"that logically continue the user's conversation and explore the next practical steps.\n\n"
            f"Rules:\n"
            f"1. Language MUST be {'Khmer' if lang_code == 'km' else 'English'}.\n"
            f"2. Each suggestion must be a direct, natural user question or prompt (5 to 12 words max).\n"
            f"3. Must be relevant to the user's latest query, previous messages, and AI answer.\n"
            f"4. If about Cambodia, prioritize authentic Cambodian locations, authorities, or terminology.\n"
            f"5. Output STRICT JSON format only: {{\"topic\": \"string\", \"suggestions\": [\"q1\", \"q2\", \"q3\", \"q4\"]}}.\n\n"
            f"User Latest Query: {user_msg}\n"
            f"AI Response Summary: {ai_ans[:300]}\n"
        )
        if refresh:
            prompt += f"Note: Generate alternative fresh follow-ups different from: {list(exclude)[:6]}.\n"

        system_instruction = (
            "Return only valid JSON with keys 'topic' and 'suggestions' (array of 4 strings). "
            "No markdown code blocks, no other text."
        )

        res = gemini_online_service.generate_with_model(
            prompt=prompt,
            system_instruction=system_instruction
        )
        if not res or not res.get("text"):
            return None

        clean_text = res["text"].strip()
        # Strip potential markdown fences
        clean_text = re.sub(r'^```(json)?\s*', '', clean_text, flags=re.MULTILINE)
        clean_text = re.sub(r'\s*```$', '', clean_text, flags=re.MULTILINE).strip()

        parsed = json.loads(clean_text)
        if isinstance(parsed, dict) and "suggestions" in parsed and isinstance(parsed["suggestions"], list):
            valid = [s.strip() for s in parsed["suggestions"] if isinstance(s, str) and len(s.strip()) > 3]
            valid = [s for s in valid if s not in exclude]
            if len(valid) >= 4:
                return {
                    "topic": str(parsed.get("topic") or "Suggested Topics").strip(),
                    "suggestions": valid[:4]
                }
        return None

    def _synthesize_contextual_suggestions(
        self,
        user_msg: str,
        ai_ans: str,
        intent: str,
        lang_code: str,
        exclude: set,
        refresh: bool = False
    ) -> Dict[str, Any]:
        """
        Deterministic, robust contextual state machine mapping conversation stages
        into logical next steps in both Khmer and English.
        """
        combined = f"{user_msg.lower()} {ai_ans.lower()}"
        is_km = lang_code == "km"

        # -------------------------------------------------------------
        # DOMAIN 1: CAMBODIAN BUSINESS & ECONOMY
        # -------------------------------------------------------------
        if (
            intent == "business_finance" or
            any(k in combined for k in [
                "business", "startup", "company", "camdx", "register", "tax", "gdt", "profit",
                "patent tax", "vat", "bakong", "khqr", "cdc", "qip",
                "អាជីវកម្ម", "ធុរកិច្ច", "ចុះបញ្ជី", "ពន្ធដារ", "ប៉ាតង់", "បាគង", "វិនិយោគ"
            ])
        ):
            # Stage B2: Specific Business Registration / CamDX
            if any(k in combined for k in ["registration", "camdx", "register", "step", "document", "authority", "fee", "ចុះបញ្ជី", "ឯកសារ", "កម្រៃ"]):
                topic = "ការចុះបញ្ជីអាជីវកម្មតាម CamDX" if is_km else "Cambodian Business Registration"
                primary_en = [
                    "Identify the relevant registration authority",
                    "Review required documents and director IDs",
                    "Check applicable registration fees and sub-decrees",
                    "Learn about the next steps after registration"
                ]
                alt_en = [
                    "How to verify digital identity with CamDigiKey",
                    "Opening a corporate bank account within 15-30 days",
                    "Understanding Ministry of Labour (MLVT) registration",
                    "Obtaining your official digital patent certificate"
                ]
                primary_km = [
                    "កំណត់ស្ថាប័នមានសមត្ថកិច្ចក្នុងការចុះបញ្ជី",
                    "ពិនិត្យបញ្ជីឯកសារតម្រូវឱ្យបានគ្រប់គ្រាន់",
                    "ពិនិត្យកម្រៃសេវាចុះបញ្ជីផ្លូវការ",
                    "ស្វែងយល់ពីជំហានបន្ទាប់ក្រោយទទួលបានវិញ្ញាបនបត្រ"
                ]
                alt_km = [
                    "របៀបផ្ទៀងផ្ទាត់អត្តសញ្ញាណឌីជីថលតាម CamDigiKey",
                    "ការបើកគណនីធនាគារសហគ្រាសក្នុងរយៈពេល ១៥-៣០ ថ្ងៃ",
                    "នីតិវិធីចុះបញ្ជីជាមួយក្រសួងការងារ និងបណ្តុះបណ្តាលវិជ្ជាជីវៈ",
                    "ការទទួលយកវិញ្ញាបនបត្រពន្ធលើប៉ាតង់ជាទម្រង់ឌីជីថល"
                ]
            # Stage B3: Taxation & GDT Obligations
            elif any(k in combined for k in ["tax", "taxation", "gdt", "vat", "top", "patent", "ពន្ធ", "អាករ", "ប៉ាតង់"]):
                topic = "ប្រព័ន្ធពន្ធដារកម្ពុជា" if is_km else "Cambodian Tax Obligations"
                primary_en = [
                    "Understand Patent Tax annual renewal deadlines",
                    "Explain Tax on Profit (ToP 20%) exemptions",
                    "Learn about monthly GDT E-Tax declarations",
                    "Check Qualified Investment Project (QIP) tax incentives"
                ]
                alt_en = [
                    "What are the thresholds for Small, Medium, and Large taxpayers?",
                    "How does 10% VAT work on domestic sales vs exports?",
                    "What is Withholding Tax (WHT) for domestic services?",
                    "How to prepare annual tax returns before March 31"
                ]
                primary_km = [
                    "ស្វែងយល់ពីកាលបរិច្ឆេទបង់ពន្ធលើប៉ាតង់ប្រចាំឆ្នាំ",
                    "ពន្យល់ពីការលើកលែងពន្ធលើប្រាក់ចំណេញ (ToP ២០%)",
                    "របៀបប្រកាសពន្ធប្រចាំខែតាមប្រព័ន្ធ GDT E-Tax",
                    "ពិនិត្យការលើកទឹកចិត្តពន្ធសម្រាប់គម្រោង QIP"
                ]
                alt_km = [
                    "តើលក្ខខណ្ឌចំណូលកំណត់អ្នកជាប់ពន្ធ តូច មធ្យម និងធំ យ៉ាងដូចម្តេច?",
                    "តើអាករលើតម្លៃបន្ថែម (VAT ១០%) អនុវត្តយ៉ាងណា?",
                    "តើពន្ធកាត់ទុក (WHT) លើថ្លៃសេវាបុគ្គលគិតយ៉ាងដូចម្តេច?",
                    "របៀបត្រៀមលិខិតប្រកាសពន្ធប្រចាំឆ្នាំមុនថ្ងៃទី ៣១ មីនា"
                ]
            # Stage B1: Initial Starting a Business
            else:
                topic = "ការចាប់ផ្តើមអាជីវកម្មនៅកម្ពុជា" if is_km else "Starting a Business in Cambodia"
                primary_en = [
                    "Understand business registration procedures",
                    "Estimate startup costs and capital requirements",
                    "Learn about Cambodian tax obligations",
                    "Create a business plan tailored to Cambodia"
                ]
                alt_en = [
                    "Explore fast-growing economic sectors in Cambodia",
                    "How to accept digital payments with Bakong KHQR",
                    "Check foreign ownership rules for Cambodian companies",
                    "Discover startup incubation at Techo Startup Center"
                ]
                primary_km = [
                    "ស្វែងយល់ពីនីតិវិធីចុះបញ្ជីអាជីវកម្ម",
                    "ប៉ាន់ស្មានដើមទុនចាប់ផ្តើមអាជីវកម្ម",
                    "ស្វែងយល់ពីកាតព្វកិច្ចពន្ធដារនៅកម្ពុជា",
                    "បង្កើតផែនការអាជីវកម្ម (Business Plan)"
                ]
                alt_km = [
                    "ស្វែងយល់ពីវិស័យសេដ្ឋកិច្ចដែលមានសក្តានុពលខ្ពស់នៅកម្ពុជា",
                    "របៀបទទួលការទូទាត់ប្រាក់តាមប្រព័ន្ធ Bakong KHQR",
                    "ពិនិត្យលក្ខខណ្ឌកម្មសិទ្ធិរបស់ជនបរទេសក្នុងការបើកក្រុមហ៊ុន",
                    "ស្វែងយល់ពីកម្មវិធីគាំទ្រអាជីវកម្មនៅមជ្ឈមណ្ឌលបណ្តុះធុរកិច្ចតេជោ"
                ]

            return self._select_candidates(topic, primary_km if is_km else primary_en, alt_km if is_km else alt_en, exclude, refresh)

        # -------------------------------------------------------------
        # DOMAIN 2: PROGRAMMING, AI & TECHNOLOGY
        # -------------------------------------------------------------
        if (
            intent in ["coding", "cambodia_tech"] or
            any(k in combined for k in [
                "laravel", "python", "javascript", "vue", "code", "ai", "rag", "embedding",
                "vector", "model", "database", "api", "bakong api", "endpoint", "architecture",
                "កូដ", "សរសេរកូដ", "កម្មវិធី", "បច្ចេកវិទ្យា"
            ])
        ):
            # Stage T3: RAG & Vector Search
            if any(k in combined for k in ["rag", "vector", "embedding", "retrieval", "chunk", "chroma", "pgvector"]):
                topic = "ប្រព័ន្ធ AI & RAG Pipeline" if is_km else "RAG Architecture & Embeddings"
                primary_en = [
                    "Choose a vector database (pgvector, Chroma, Qdrant)",
                    "Prepare and chunk documents effectively",
                    "Generate embeddings with all-MiniLM or OpenAI",
                    "Retrieve relevant documents for AI responses"
                ]
                alt_en = [
                    "How to tune similarity search threshold and top-k",
                    "Implementing hybrid keyword + vector retrieval",
                    "Evaluating RAG response accuracy and hallucination",
                    "How to handle real-time dynamic knowledge updates"
                ]
                primary_km = [
                    "ជ្រើសរើស Vector Database (pgvector, Chroma, Qdrant)",
                    "រៀបចំ និងកាត់បំបែកឯកសារ (Chunking)",
                    "បង្កើត Embeddings សម្រាប់ទិន្នន័យ",
                    "ទាញយកឯកសារពាក់ព័ន្ធមកឆ្លើយតបសំណួរ (Retrieval)"
                ]
                alt_km = [
                    "របៀបកំណត់កម្រិតភាពស្រដៀងគ្នា Similarity Threshold និង Top-K",
                    "ការបញ្ចូលគ្នារវាងការស្វែងរកតាមពាក្យគន្លឹះ និងវ៉ិចទ័រ (Hybrid Search)",
                    "ការវាស់វែងភាពត្រឹមត្រូវ និងទប់ស្កាត់ការឆ្លើយមិនពិត (Anti-hallucination)",
                    "របៀបធ្វើបច្ចុប្បន្នភាពទិន្នន័យចំណេះដឹងថ្មីៗក្នុងប្រព័ន្ធ"
                ]
            # Stage T1: Building AI Application with Laravel / Vue
            elif any(k in combined for k in ["laravel", "architecture", "build an ai", "vue", "fastapi"]):
                topic = "ការបង្កើតកម្មវិធី AI ជាមួយ Laravel" if is_km else "Building AI Application with Laravel"
                primary_en = [
                    "Design the AI application architecture",
                    "Connect an AI model API (Gemini or OpenAI)",
                    "Implement conversation history in database",
                    "Add Retrieval-Augmented Generation (RAG)"
                ]
                alt_en = [
                    "Integrate Bakong KHQR Open API for checkout payments",
                    "Implement Server-Sent Events (SSE) for streaming chat",
                    "Set up Laravel Sanctum API authentication",
                    "Deploy the application with Docker and Nginx"
                ]
                primary_km = [
                    "រៀបចំស្ថាបត្យកម្មកម្មវិធី AI (Architecture)",
                    "តភ្ជាប់ API របស់ AI Model (Gemini ឬ OpenAI)",
                    "បង្កើតប្រព័ន្ធរក្សាទុកប្រវត្តិសន្ទនា (History)",
                    "បញ្ចូលប្រព័ន្ធ Retrieval-Augmented Generation (RAG)"
                ]
                alt_km = [
                    "ភ្ជាប់ប្រព័ន្ធទូទាត់ Bakong KHQR Open API",
                    "បង្កើតការបញ្ជូនអក្សរផ្ទាល់ (SSE Streaming Response)",
                    "រៀបចំប្រព័ន្ធផ្ទៀងផ្ទាត់សិទ្ធិដោយប្រើ Laravel Sanctum",
                    "ការដាក់ឱ្យដំណើរការប្រព័ន្ធ (Deploy) តាម Docker និង Nginx"
                ]
            # Stage T2: General Coding, Algorithms & Software
            else:
                topic = "វិស្វកម្មសូហ្វវែរ & ក្បួនដោះស្រាយ" if is_km else "Software Engineering & Code"
                primary_en = [
                    "Write unit tests for this implementation",
                    "Optimize performance and reduce time complexity",
                    "Add error handling and input validation",
                    "Design the database schema and models"
                ]
                alt_en = [
                    "How to structure this into modular services",
                    "Analyze Big-O time and space complexity",
                    "Containerize this service with Docker",
                    "Add automated CI/CD deployment pipeline"
                ]
                primary_km = [
                    "សរសេរ Unit Test សម្រាប់ផ្ទៀងផ្ទាត់មុខងារកូដនេះ",
                    "បង្កើនល្បឿន និងកាត់បន្ថយភាពស្មុគស្មាញ (Optimize)",
                    "បន្ថែមប្រព័ន្ធគ្រប់គ្រងកំហុស (Error Handling)",
                    "រៀបចំទម្រង់ Database Schema និង Data Models"
                ]
                alt_km = [
                    "របៀបរៀបចំកូដឱ្យមានរចនាសម្ព័ន្ធស្អាត (Modular Services)",
                    "វិភាគភាពស្មុគស្មាញកូដ Big-O Time & Space",
                    "ការវេចខ្ចប់កូដជាកញ្ចប់ Docker Container",
                    "ការរៀបចំប្រព័ន្ធស្វ័យប្រវត្តិកម្ម CI/CD Deployment"
                ]

            return self._select_candidates(topic, primary_km if is_km else primary_en, alt_km if is_km else alt_en, exclude, refresh)

        # -------------------------------------------------------------
        # DOMAIN 3: CAMBODIA GOVERNMENT & PUBLIC SERVICES
        # -------------------------------------------------------------
        if (
            intent == "cambodia_government" or
            any(k in combined for k in [
                "passport", "visa", "driver license", "license", "sangkat", "gdi", "mpwt",
                "owso", "public service", "ministry", "certificate", "id card",
                "លិខិតឆ្លងដែន", "ប៉ាស្ព័រ", "ទិដ្ឋាការ", "បណ្ណបើកបរ", "សង្កាត់", "សំបុត្រកំណើត"
            ])
        ):
            # Stage G1: Passports (GDI)
            if any(k in combined for k in ["passport", "gdi", "passports", "លិខិតឆ្លងដែន", "ប៉ាស្ព័រ"]):
                topic = "សេវាធ្វើលិខិតឆ្លងដែនខ្មែរ (GDI)" if is_km else "Cambodian Passport Services (GDI)"
                primary_en = [
                    "Find GDI passport offices and branch locations",
                    "Check required Family Book and Khmer ID documents",
                    "Understand regular vs expedited processing fees",
                    "Review passport requirements for children under 18"
                ]
                alt_en = [
                    "Can I renew an expired Cambodian passport online?",
                    "What are the office hours for Aeon Mall Sen Sok GDI branch?",
                    "How many passport photos are required and photo guidelines?",
                    "What to do if your Cambodian passport is lost abroad"
                ]
                primary_km = [
                    "ស្វែងរកទីតាំងធ្វើលិខិតឆ្លងដែន និងសាខា GDI",
                    "ពិនិត្យឯកសារតម្រូវ (សៀវភៅស្នាក់នៅ/គ្រួសារ និងអត្តសញ្ញាណប័ណ្ណ)",
                    "ស្វែងយល់ពីកម្រៃសេវាធម្មតា និងសេវាបន្ទាន់",
                    "លក្ខខណ្ឌធ្វើលិខិតឆ្លងដែនសម្រាប់កុមារក្រោម ១៨ ឆ្នាំ"
                ]
                alt_km = [
                    "តើអាចបន្តសុពលភាពលិខិតឆ្លងដែនតាមអនឡាញបានទេ?",
                    "តើសាខាផ្សារទំនើបអ៊ីអនសែនសុខបើកម៉ោងប៉ុន្មានខ្លះ?",
                    "តើត្រូវប្រើរូបថតប៉ុន្មានសន្លឹក និងមានទម្រង់បែបណា?",
                    "តើត្រូវធ្វើដូចម្តេចប្រសិនបើបាត់លិខិតឆ្លងដែននៅក្រៅប្រទេស?"
                ]
            # Stage G2: Visas (MFAIC e-Visa)
            elif any(k in combined for k in ["visa", "visas", "evisa", "arrival", "immigration", "ទិដ្ឋាការ", "អន្តោប្រវេសន៍"]):
                topic = "ទិដ្ឋាការកម្ពុជា e-Visa & Entry" if is_km else "Cambodia Visas & E-Visa"
                primary_en = [
                    "Apply through official evisa.gov.kh portal",
                    "Compare Tourist (T) vs Business (E) visas",
                    "Check visa extension rules and requirements",
                    "Prepare documents needed for Visa on Arrival"
                ]
                alt_en = [
                    "What is the official e-Visa processing fee and timeline?",
                    "Which international border checkpoints accept e-Visa?",
                    "How to extend an Ordinary E visa for 6 or 12 months",
                    "Required validity on foreign passport before entering Cambodia"
                ]
                primary_km = [
                    "របៀបស្នើសុំទិដ្ឋាការតាមគេហទំព័រផ្លូវការ evisa.gov.kh",
                    "ប្រៀបធៀបរវាងទិដ្ឋាការទេសចរណ៍ (T) និងទិដ្ឋាការធុរកិច្ច (E)",
                    "ពិនិត្យលក្ខខណ្ឌ និងនីតិវិធីនៃការបន្តសុពលភាពទិដ្ឋាការ",
                    "ឯកសារតម្រូវសម្រាប់ធ្វើទិដ្ឋាការពេលមកដល់ (Visa on Arrival)"
                ]
                alt_km = [
                    "តើតម្លៃសេវា និងរយៈពេលរង់ចាំ e-Visa ផ្លូវការប៉ុន្មានដែរ?",
                    "តើច្រកទ្វារព្រំដែនណាខ្លះដែលទទួលស្គាល់ e-Visa?",
                    "របៀបបន្តទិដ្ឋាការធម្មតា E រយៈពេល ៦ ឬ ១២ ខែ",
                    "លក្ខខណ្ឌសុពលភាពលិខិតឆ្លងដែនមុនពេលចូលកម្ពុជា"
                ]
            # Stage G3: Driver License / MPWT / OWSO
            else:
                topic = "សេវាសាធារណៈ & បណ្ណបើកបរ MPWT" if is_km else "Public Services & Driver License"
                primary_en = [
                    "Locate MPWT driver license service centers (Aeon malls)",
                    "Convert a foreign driver's license to Cambodian license",
                    "Check required medical test and identification documents",
                    "Review renewal validity periods (5 vs 10 years)"
                ]
                alt_en = [
                    "How to access Sangkat One Window Service Offices (OWSO)",
                    "Procedures for issuing certified birth certificates",
                    "Registering residential address at local commune",
                    "Vehicle inspection (check) and registration procedures"
                ]
                primary_km = [
                    "ស្វែងរកទីតាំងបន្តបណ្ណបើកបរ MPWT (ផ្សារទំនើបអ៊ីអន)",
                    "ការប្តូរបណ្ណបើកបរអន្តរជាតិមកជាបណ្ណបើកបរកម្ពុជា",
                    "ពិនិត្យការពិនិត្យសុខភាព និងឯកសារអត្តសញ្ញាណតម្រូវ",
                    "សុពលភាពនៃការបន្តបណ្ណបើកបរ (៥ ឆ្នាំ ឬ ១០ ឆ្នាំ)"
                ]
                alt_km = [
                    "របៀបប្រើប្រាស់សេវាច្រកចេញចូលតែមួយនៅសង្កាត់ (OWSO)",
                    "នីតិវិធីស្នើសុំសំបុត្រកំណើតផ្លូវការ",
                    "ការចុះបញ្ជីស្នាក់នៅជាមួយអាជ្ញាធរមូលដ្ឋាន",
                    "នីតិវិធីឆែកឆេរត្រួតពិនិត្យលក្ខណៈបច្ចេកទេសយានយន្ត"
                ]

            return self._select_candidates(topic, primary_km if is_km else primary_en, alt_km if is_km else alt_en, exclude, refresh)

        # -------------------------------------------------------------
        # DOMAIN 4: CAMBODIA EDUCATION & RESEARCH
        # -------------------------------------------------------------
        if (
            intent == "cambodia_education" or
            any(k in combined for k in [
                "bacii", "exam", "grade 12", "rupp", "itc", "cadt", "university", "moeys",
                "បាក់ឌុប", "ប្រឡង", "ថ្នាក់ទី១២", "សាកលវិទ្យាល័យ", "តិចណូ", "ក្រសួងអប់រំ"
            ])
        ):
            topic = "ការអប់រំ & ការប្រឡងបាក់ឌុប" if is_km else "Cambodian Education & BacII Exam"
            primary_en = [
                "Compare Science track vs Social Science track subjects",
                "Understand national grading formula (Grade A to E)",
                "Practice high school mathematics exam problems",
                "Review official MoEYS exam regulations and rules"
            ]
            alt_en = [
                "Explore engineering degree majors at ITC (សាលាតិចណូ)",
                "Apply for computer science degrees at RUPP",
                "Check CADT digital technology scholarships",
                "Explore higher education opportunities in Cambodia"
            ]
            primary_km = [
                "ប្រៀបធៀបមុខវិជ្ជាថ្នាក់វិទ្យាសាស្ត្រ និងវិទ្យាសាស្ត្រសង្គម",
                "ស្វែងយល់ពីរូបមន្តគណនានិទ្ទេសប្រឡង (និទ្ទេស A ដល់ E)",
                "លំហាត់គណិតវិទ្យាត្រៀមប្រឡងបាក់ឌុបថ្នាក់ទី ១២",
                "ពិនិត្យបទបញ្ញត្តិ និងវិន័យផ្លូវការរបស់ក្រសួងអប់រំ"
            ]
            alt_km = [
                "ស្វែងយល់ពីជំនាញវិស្វកម្មនៅវិទ្យាស្ថានតិចណូ (ITC)",
                "ការដាក់ពាក្យរៀនវិទ្យាសាស្ត្រកុំព្យូទ័រនៅសាកលវិទ្យាល័យភូមិន្ទភ្នំពេញ (RUPP)",
                "ព័ត៌មានអាហារូបករណ៍បច្ចេកវិទ្យាឌីជីថលនៅបណ្ឌិត្យសភា CADT",
                "ស្វែងយល់ពីឱកាសសិក្សាថ្នាក់ឧត្តមសិក្សានាំមុខគេនៅកម្ពុជា"
            ]
            return self._select_candidates(topic, primary_km if is_km else primary_en, alt_km if is_km else alt_en, exclude, refresh)

        # -------------------------------------------------------------
        # DOMAIN 5: KHMER LANGUAGE & TRANSLATION
        # -------------------------------------------------------------
        if (
            intent in ["khmer_language", "translation"] or
            any(k in combined for k in [
                "letter", "translate", "translation", "grammar", "orthography", "chuon nath",
                "លិខិត", "បកប្រែ", "អក្ខរាវិរុទ្ធ", "វេយ្យាករណ៍", "ជួន ណាត", "ភាសាខ្មែរ"
            ])
        ):
            topic = "ភាសាខ្មែរ & ការសរសេរលិខិតរដ្ឋបាល" if is_km else "Khmer Language & Official Writing"
            primary_en = [
                "Review royal motto header format for official letters",
                "Choose correct hierarchical salutation (សូមគោរពជូន vs សូមជម្រាបជូន)",
                "Structure main body and reference section properly",
                "Write respectful administrative concluding remarks"
            ]
            alt_en = [
                "Consult Chuon Nath dictionary spelling rules",
                "Understand first vs second consonant series vowels (ពួក អ និង ពួក អ៊)",
                "How to type Khmer Unicode subscripts (ជើងអក្សរ) accurately",
                "Review Khmer diacritical marks (បន្តក់, សំយោគសញ្ញា, ត្រីស័ព្ទ)"
            ]
            primary_km = [
                "ទម្រង់ពាក្យស្លោកជាតិនៅក្បាលលិខិតផ្លូវការ",
                "ការប្រើពាក្យគួរសមតាមឋានានុក្រម (សូមគោរពជូន vs សូមជម្រាបជូន)",
                "រចនាសម្ព័ន្ធកម្មវត្ថុ យោង និងខ្លឹមសារលិខិត",
                "ពាក្យបញ្ចប់ការគោរពតាមបែបបទរដ្ឋបាលខ្មែរ"
            ]
            alt_km = [
                "ក្បួនអក្ខរាវិរុទ្ធតាមវចនានុក្រមសម្តេចសង្ឃរាជ ជួន ណាត",
                "ស្វែងយល់ពីស្រៈនិស្ស័យតាមពួកព្យញ្ជនៈ (ពួក អ និង ពួក អ៊)",
                "របៀបវាយជើងអក្សរខ្មែរ (Khmer Unicode) ឱ្យបានត្រឹមត្រូវ",
                "ការប្រើប្រាស់វណ្ណយុត្តិ និងសញ្ញាសម្គាល់ (បន្តក់, សំយោគសញ្ញា, ត្រីស័ព្ទ)"
            ]
            return self._select_candidates(topic, primary_km if is_km else primary_en, alt_km if is_km else alt_en, exclude, refresh)

        # -------------------------------------------------------------
        # DOMAIN 6: MATHEMATICS & SCIENCE
        # -------------------------------------------------------------
        if (
            intent == "math_science" or
            any(k in combined for k in [
                "gradient descent", "derivative", "calculus", "integral", "matrix", "equation",
                "algorithm", "big-o", "math", "physics", "គណិតវិទ្យា", "រូបវិទ្យា", "គណនា"
            ])
        ):
            topic = "គណិតវិទ្យា & Data Science" if is_km else "Mathematics & Machine Learning"
            primary_en = [
                "Derive the loss function partial derivatives step-by-step",
                "Implement Gradient Descent in Python from scratch",
                "Compare Batch, Stochastic, and Mini-batch variants",
                "Tune the learning rate hyperparameter and momentum"
            ]
            alt_en = [
                "Analyze Big-O time and space complexity",
                "How does Backpropagation calculate gradients across layers?",
                "Explain eigenvalues and eigenvectors with visual intuition",
                "Compare Newton-Raphson optimization vs Gradient Descent"
            ]
            primary_km = [
                "របៀបគណនាដេរីវេដោយផ្នែកនៃ Loss Function មួយជំហានម្តងៗ",
                "សរសេរកូដ Gradient Descent ក្នុង Python ដោយផ្ទាល់",
                "ប្រៀបធៀប Batch, Stochastic និង Mini-batch Gradient Descent",
                "ការកែសម្រួល Learning Rate និង Momentum ឱ្យប្រសើរ"
            ]
            alt_km = [
                "ការវិភាគភាពស្មុគស្មាញក្បួនដោះស្រាយ Big-O Notation",
                "របៀបដែល Backpropagation គណនា Gradient ឆ្លងកាត់ Layers",
                "ការពន្យល់ពី Eigenvalues និង Eigenvectors យ៉ាងងាយយល់",
                "ប្រៀបធៀបវិធីសាស្ត្រ Newton-Raphson ជាមួយ Gradient Descent"
            ]
            return self._select_candidates(topic, primary_km if is_km else primary_en, alt_km if is_km else alt_en, exclude, refresh)

        # -------------------------------------------------------------
        # DOMAIN 7: CAMBODIA TOURISM & TRAVEL (DEFAULT FOCUS)
        # -------------------------------------------------------------
        # Stage T3: Angkor Wat Specific
        if any(k in combined for k in ["angkor wat", "angkor", "temple", "sunrise", "ticket", "អង្គរវត្ត", "ប្រាសាទអង្គរ"]):
            topic = "ប្រាសាទអង្គរវត្ត & បេតិកភណ្ឌ" if is_km else "Angkor Wat & Cultural Heritage"
            primary_en = [
                "Learn about Angkor Wat's history and architecture",
                "Discover the best time and spot for sunrise",
                "Understand temple entrance ticket options (Angkor Pass)",
                "Explore nearby temples around the Small and Grand Circuit"
            ]
            alt_en = [
                "What is the dress code for visiting ancient Khmer temples?",
                "Discover the intricate stone carvings of Banteay Srei",
                "Explore the gigantic smiling faces of the Bayon Temple",
                "Visit the jungle-entangled ruins of Ta Prohm"
            ]
            primary_km = [
                "ស្វែងយល់អំពីប្រវត្តិសាស្ត្រ និងស្ថាបត្យកម្មអង្គរវត្ត",
                "ស្វែងរកពេលវេលា និងទីតាំងល្អបំផុតសម្រាប់មើលថ្ងៃរះ",
                "ស្វែងយល់ពីជម្រើសតម្លៃសំបុត្រចូលទស្សនាប្រាសាទ (Angkor Pass)",
                "ទស្សនាប្រាសាទបុរាណជុំវិញវង់តូច និងវង់ធំ"
            ]
            alt_km = [
                "តើត្រូវស្លៀកពាក់បែបណាពេលចូលទស្សនាប្រាសាទបុរាណ?",
                "ស្វែងយល់ពីក្បាច់ចម្លាក់ថ្មដ៏ល្អប្រណីតនៅប្រាសាទបន្ទាយស្រី",
                "ទស្សនាប្រាសាទបាយ័ន និងព្រះភ័ក្ត្រញញឹមទាំង ៥៤",
                "ទស្សនាប្រាសាទតាព្រហ្មដែលមានដើមឈើដុះលើថ្មបុរាណ"
            ]
        # Stage T2: Siem Reap Trip Planning
        elif any(k in combined for k in ["siem reap", "itinerary", "plan a trip", "3-day", "travel budget", "សៀមរាប", "ដំណើរកម្សាន្ត"]):
            topic = "ដំណើរកម្សាន្តនៅសៀមរាប" if is_km else "Siem Reap Travel Planning"
            primary_en = [
                "Create a 3-day Siem Reap cultural itinerary",
                "Find transportation from Phnom Penh to Siem Reap",
                "Estimate hotel and food costs for your stay",
                "Explore temples around Angkor Archaeological Park"
            ]
            alt_en = [
                "Where to find authentic Khmer cuisine and night markets in Siem Reap",
                "Take a floating village boat tour on the Tonle Sap Lake",
                "Experience the famous Phare Cambodian Circus show",
                "Explore Kulen Mountain sacred waterfall and River of a Thousand Lingas"
            ]
            primary_km = [
                "រៀបចំគម្រោងដើរលេង ៣ ថ្ងៃនៅសៀមរាប",
                "របៀបធ្វើដំណើរពីភ្នំពេញទៅសៀមរាប",
                "ការប៉ាន់ស្មានការចំណាយលើសណ្ឋាគារ និងអាហារ",
                "ស្វែងយល់ពីប្រាសាទបុរាណជុំវិញឧទ្យានអង្គរ"
            ]
            alt_km = [
                "កន្លែងញ៉ាំអាហារខ្មែរឆ្ងាញ់ៗ និងផ្សាររាត្រីនៅសៀមរាប",
                "ដំណើរកម្សាន្តតាមទូកទស្សនាភូមិបណ្តែតទឹកបឹងទន្លេសាប",
                "ទស្សនាការសម្តែងសៀកហ្វារ (Phare Circus) ដ៏ល្បីល្បាញ",
                "ដើរលេងឧទ្យានជាតិភ្នំគូលែន និងស្ទឹងលិង្គមួយពាន់"
            ]
        # Stage T4: Phnom Penh / Sihanoukville / Coastal
        elif any(k in combined for k in ["phnom penh", "kampot", "kep", "koh rong", "sihanoukville", "beach", "ភ្នំពេញ", "កំពត", "កែប", "កោះរ៉ុង"]):
            topic = "រាជធានីភ្នំពេញ និងតំបន់ឆ្នេរ" if is_km else "Phnom Penh & Coastal Cambodia"
            primary_en = [
                "Explore the Royal Palace and Silver Pagoda in Phnom Penh",
                "Find speed ferry schedules to Koh Rong island",
                "Taste fresh Kep crab with Kampot green pepper",
                "Visit Bokor Mountain national park and historic hill station"
            ]
            alt_en = [
                "Take a relaxing sunset boat cruise on the Mekong River",
                "Discover Phnom Penh street food and vibrant night markets",
                "Compare Koh Rong vs Koh Rong Sanloem for a beach vacation",
                "Explore historical exhibits at the National Museum of Cambodia"
            ]
            primary_km = [
                "ទស្សនាព្រះបរមរាជវាំង និងវត្តព្រះកែវមរកតនៅភ្នំពេញ",
                "ស្វែងរកកាលវិភាគអូប័រល្បឿនលឿនទៅកាន់កោះរ៉ុង",
                "ភ្លក្សរសជាតិក្តាមឆាម្រេចខ្ចីដ៏ល្បីល្បាញនៅខេត្តកែប",
                "ដើរលេងឧទ្យានជាតិភ្នំបូកគោ និងសំណង់ប្រវត្តិសាស្ត្រ"
            ]
            alt_km = [
                "ជិះទូកកម្សាន្តមើលថ្ងៃលិចតាមដងទន្លេមេគង្គ",
                "ស្វែងរកអាហារតាមផ្លូវ (Street Food) និងផ្សាររាត្រីនៅភ្នំពេញ",
                "ប្រៀបធៀបរវាងកោះរ៉ុង និងកោះរ៉ុងសន្លឹមសម្រាប់សម្រាកលំហែ",
                "ទស្សនាសារមន្ទីរជាតិកម្ពុជា និងវត្ថុបុរាណខ្មែរដ៏កម្រ"
            ]
        # Stage T1: Initial Cambodia Tourism Focus
        else:
            topic = "ទេសចរណ៍ និងវប្បធម៌កម្ពុជា" if is_km else "Cambodia Tourism & Culture"
            primary_en = [
                "Explore Cambodia's top tourist destinations",
                "Plan a trip to Siem Reap and Angkor temples",
                "Discover Angkor Wat's history and royal marvels",
                "Estimate a Cambodia travel budget and daily costs"
            ]
            alt_en = [
                "Overview of the 25 administrative divisions of Cambodia",
                "What authentic Khmer dishes are must-try for visitors?",
                "Currency tips: Using US Dollars vs Cambodian Riel",
                "Best times of year to visit Cambodia and weather guide"
            ]
            primary_km = [
                "ស្វែងយល់ពីរមណីយដ្ឋានទេសចរណ៍ល្បីៗនៅកម្ពុជា",
                "រៀបចំគម្រោងដំណើរកម្សាន្តទៅសៀមរាប និងអង្គរ",
                "ស្វែងយល់ពីប្រវត្តិសាស្ត្រអង្គរវត្តដ៏រុងរឿង",
                "ការប៉ាន់ស្មានកញ្ចប់ថវិកាដើរលេងនៅកម្ពុជា"
            ]
            alt_km = [
                "ទិដ្ឋភាពទូទៅនៃរាជធានី-ខេត្តទាំង ២៥ នៅកម្ពុជា",
                "តើម្ហូបខ្មែរប្រពៃណីណាខ្លះដែលមិនគួររំលង?",
                "ការណែនាំពីការចាយលុយដុល្លារ និងប្រាក់រៀល",
                "រដូវកាលល្អបំផុតសម្រាប់ដំណើរកម្សាន្តនៅកម្ពុជា"
            ]

        return self._select_candidates(topic, primary_km if is_km else primary_en, alt_km if is_km else alt_en, exclude, refresh)

    def _select_candidates(
        self,
        topic: str,
        primary_list: List[str],
        alt_list: List[str],
        exclude: set,
        refresh: bool
    ) -> Dict[str, Any]:
        """Select 4 clean, unique suggestions taking exclusion and refresh into account."""
        if refresh:
            candidates = [c for c in alt_list if c not in exclude]
            if len(candidates) < 4:
                candidates += [c for c in primary_list if c not in exclude]
            if len(candidates) < 4:
                candidates = alt_list + primary_list
        else:
            candidates = [c for c in primary_list if c not in exclude]
            if len(candidates) < 4:
                candidates += [c for c in alt_list if c not in exclude]
            if len(candidates) < 4:
                candidates = primary_list + alt_list

        # Deduplicate while preserving order
        seen = set()
        unique = []
        for c in candidates:
            if c not in seen:
                seen.add(c)
                unique.append(c)

        return {
            "topic": topic,
            "suggestions": unique[:4]
        }

suggestion_service = SuggestionService()
