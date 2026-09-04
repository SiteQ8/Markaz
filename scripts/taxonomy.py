"""Curated domain taxonomy for the Markaz catalog.

Every original repository under the SiteQ8 account is assigned to exactly one
domain. Forked and mirrored repositories are excluded from the catalog and
listed separately so that upstream work is never presented as original
research.
"""

DOMAINS = [
    ("kuwait-gcc", "Kuwait and GCC Frameworks", "الأطر الكويتية والخليجية",
     "Regulatory frameworks, control catalogues and policy sets specific to Kuwait and the wider Gulf.",
     "أطر تنظيمية وكتالوجات ضوابط ومجموعات سياسات تخص الكويت ومنطقة الخليج."),
    ("compliance", "Global Compliance", "الامتثال العالمي",
     "Tooling for internationally recognised control frameworks and benchmarks.",
     "أدوات تخدم أطر الضوابط والمعايير المعترف بها دولياً."),
    ("ics-ot", "ICS, OT and IoT", "أنظمة التحكم الصناعي والتشغيل",
     "Industrial control, operational technology and connected device security.",
     "أمن أنظمة التحكم الصناعي وتقنية التشغيل والأجهزة المتصلة."),
    ("crypto", "Cryptography and PQC", "التعمية والجاهزية الكمية",
     "Cryptographic inventory, transport security and post quantum readiness.",
     "جرد الخوارزميات التعموية وأمن النقل والجاهزية لما بعد الحوسبة الكمية."),
    ("dfir", "Forensics and Threat Hunting", "الأدلة الرقمية وصيد التهديدات",
     "Incident response, network forensics and detection engineering.",
     "الاستجابة للحوادث والأدلة الجنائية الشبكية وهندسة الكشف."),
    ("exposure", "Exposure and Brand Protection", "الانكشاف وحماية العلامة",
     "Secret leakage, phishing, domain abuse and sensitive data discovery.",
     "تسريب الأسرار والتصيّد وإساءة استخدام النطاقات واكتشاف البيانات الحساسة."),
    ("offensive", "Offensive Security", "الأمن الهجومي",
     "Penetration testing, vulnerability assessment and adversary tooling.",
     "اختبار الاختراق وتقييم الثغرات وأدوات محاكاة الخصم."),
    ("cloud", "Cloud and Infrastructure", "السحابة والبنية التحتية",
     "Cloud exposure auditing, infrastructure as code and platform security.",
     "تدقيق الانكشاف السحابي والبنية التحتية كشيفرة وأمن المنصات."),
    ("hardening", "System Hardening", "تحصين الأنظمة",
     "Operating system and platform hardening against recognised benchmarks.",
     "تحصين أنظمة التشغيل والمنصات وفق المعايير المعتمدة."),
    ("architecture", "Security Architecture", "معمارية الأمن",
     "Trust zone modelling, threat modelling and reference blueprints.",
     "نمذجة مناطق الثقة ونمذجة التهديدات والمخططات المرجعية."),
    ("governance", "Governance and Leadership", "الحوكمة والقيادة",
     "Programme management, executive reporting and security strategy.",
     "إدارة البرامج والتقارير التنفيذية والاستراتيجية الأمنية."),
    ("ai-security", "AI and Agent Security", "أمن الذكاء الاصطناعي والوكلاء",
     "Security of language models, agent protocols and AI assisted operations.",
     "أمن النماذج اللغوية وبروتوكولات الوكلاء والعمليات المدعومة بالذكاء الاصطناعي."),
    ("discovery", "Asset and Network Discovery", "اكتشاف الأصول والشبكات",
     "Inventory, topology mapping and continuous asset visibility.",
     "الجرد ورسم الطوبولوجيا والرؤية المستمرة للأصول."),
    ("education", "Education and Awareness", "التعليم والتوعية",
     "Training material, hands on lessons and public awareness resources.",
     "مواد تدريبية ودروس تطبيقية وموارد توعية عامة."),
    ("community", "Community and Civic", "المجتمع والخدمات المدنية",
     "Open resources built for the Kuwaiti and Arabic speaking public.",
     "موارد مفتوحة بنيت لخدمة الجمهور الكويتي والناطق بالعربية."),
]

ASSIGN = {
    # Kuwait and GCC frameworks
    "Kuwait-NBCC": "kuwait-gcc",
    "CORF": "kuwait-gcc",
    "cbk-corf-toolkit": "kuwait-gcc",
    "corf-compliance-tool": "kuwait-gcc",
    "CBK-Compliance-Toolkit": "kuwait-gcc",
    "kuwait-financial-frameworks": "kuwait-gcc",
    "CyberPolicy-KW": "kuwait-gcc",
    "CIS-Kuwait-Assessment": "kuwait-gcc",
    "NCA-ECC-Crosswalk": "kuwait-gcc",
    "sama-csf-assessment": "kuwait-gcc",
    "arabic-infosec-policies": "kuwait-gcc",
    "arabic-cis-controls-repo": "kuwait-gcc",
    "M365-Defender-Kuwait-Hunting": "kuwait-gcc",
    "M365-PCI-Kuwait-Scanner": "kuwait-gcc",
    "KWTCyberWatch": "kuwait-gcc",
    "KWT5h13ld": "kuwait-gcc",
    "KWTWatch": "kuwait-gcc",

    # Global compliance
    "CIS-Audit-Tool": "compliance",
    "CIS-Benchmark-Compliance-Checker": "compliance",
    "cis-controls-platform": "compliance",
    "cis-controls-tool": "compliance",
    "cis-edu-tool": "compliance",
    "cisdash": "compliance",
    "secureops-compass": "compliance",
    "SecAudit": "compliance",

    # ICS, OT and IoT
    "ics-iot-ot-hardening": "ics-ot",
    "ics-iot-ot-framework": "ics-ot",
    "0xPlant": "ics-ot",
    "ConduitShield": "ics-ot",
    "FalconOT": "ics-ot",
    "OpenICS-Atlas": "ics-ot",
    "OTAUD": "ics-ot",

    # Cryptography
    "miftah": "crypto",
    "TLSGuard": "crypto",
    "tls-cert-expiry-radar": "crypto",

    # Forensics and threat hunting
    "Athar": "dfir",
    "NetHawk": "dfir",
    "LLM-DFIR": "dfir",
    "ShadowPulse": "dfir",
    "M365-Defender-Hunting": "dfir",
    "soc-tools": "dfir",
    "secopsdash": "dfir",
    "field-manual": "dfir",
    "Ghirbal": "dfir",

    # Exposure and brand protection
    "LeakHound": "exposure",
    "Kashif": "exposure",
    "PhishBOT": "exposure",
    "PhishHunter": "exposure",
    "PhishWatch": "exposure",
    "phishing": "exposure",
    "domain-squatting": "exposure",
    "m365-pci-pan-hunt": "exposure",

    # Offensive security
    "Marsad": "offensive",
    "vulnscan-framework": "offensive",
    "owasp-top10-scanner": "offensive",
    "APIShield": "offensive",
    "alenezi-tool": "offensive",
    "pythonpentools": "offensive",
    "ctf-notes": "offensive",
    "cvedb-api-dashboard": "offensive",
    "ThreatMapper": "offensive",
    "SiteQ8-CyberToolkit": "offensive",

    # Cloud and infrastructure
    "Raqib": "cloud",
    "InfraCode": "cloud",
    "S7aba": "cloud",
    "openshift": "cloud",
    "secure-api-service": "cloud",

    # Hardening
    "hardnix": "hardening",
    "HardHat": "hardening",
    "PowerShield": "hardening",

    # Architecture
    "Mimar": "architecture",
    "Naqsha": "architecture",
    "Hisn": "architecture",
    "SecureArch": "architecture",
    "secure-architecture-blueprints": "architecture",

    # Governance
    "Diwan": "governance",
    "CISO-Dashboard": "governance",
    "ciso-executive-dashboard": "governance",
    "cyberstrategy-workbench": "governance",
    "security-leadership-panel": "governance",

    # AI and agent security
    "KaliMCP": "ai-security",
    "MCP-CTF-Demo": "ai-security",
    "CloudMCP-Arsenal": "ai-security",
    "claude-recommendations": "ai-security",

    # Discovery
    "NetMap": "discovery",
    "LANEye": "discovery",
    "nmap": "discovery",
    "python_network": "discovery",
    "osint": "discovery",
    "OSINT-Tools": "discovery",
    "PublicEye": "discovery",

    # Education
    "Wa3i": "education",
    "Manara": "education",
    "AZ-900-Azure-Fundamentals": "education",
    "CyberArsenal": "education",
    "InfoSecPython": "education",
    "powershell": "education",
    "passwordcracking": "education",

    # Community
    "KW-OS": "community",
    "NewKuwaitCity-SmartSecure": "community",
    "Wain": "community",
    "MAI": "community",
    "ArabWatch": "community",
    "daily-ayah": "community",
    "duaarepo": "community",
    "Hawqala": "community",
    "sp": "community",
}

# Repositories deliberately kept out of the catalogue.
EXCLUDE = {"SiteQ8", "Markaz"}


def maturity(repo):
    """Classify how far along a repository is, from its own metadata."""
    size = repo["size"]
    has_desc = bool(repo["description"])
    if size >= 400 and has_desc and repo["has_pages"]:
        return "flagship"
    if size >= 40 and has_desc:
        return "active"
    return "seed"
