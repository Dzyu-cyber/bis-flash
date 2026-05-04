export const translations = {
  en: {
    title: "AI-Powered BIS Standard Discovery",
    subtitle: "A highly-precise semantic search engine designed to navigate the Bureau of Indian Standards corpus. Utilizing state-of-the-art vector embeddings and Gemini 1.5 Pro rationale generation.",
    searchPlaceholder: "Search for BIS standards (e.g., 'EV charging safety')...",
    identifiedStandards: "Identified Standards",
    found: "found",
    viewDocument: "View Document",
    aiRationale: "AI RATIONALE & EXTRACTION",
    latency: "Retrival Latency",
    relevance: "Avg Relevance",
    coverage: "Text Coverage",
    pipeline: "Pipeline Execution",
    search: "Search",
    searchTitle: "Semantic Standard Search",
    searchDescription: "Enter a product description, use case, or technical query. The AI will traverse the vector space to identify the most relevant BIS standards, providing a detailed rationale.",
    analyzing: "Analyzing",
    exampleQueries: "Example queries:",
    match: "Match",
    distribution: "Semantic Similarity Distribution",
    reasoningTrace: "Reasoning Trace",
    keyEntities: "Key Entities Extracted",
    results: [
      {
        id: "IS 16221 (Part 1) : 2015",
        title: "Electric Vehicle Conductive Charging System Part 1 General Requirements",
        category: "Automotive",
        summary: "Specifies the general requirements for conductive charging of electric vehicles. It covers the characteristics and operating conditions of the supply device and the connection to the EV.",
        rationale: "The user query specifically mentions 'charging stations' and 'safety'. This standard directly addresses the general requirements for EV charging, which fundamentally encompasses safety protocols and operational conditions for the supply device. The vector similarity is exceptionally high due to exact multi-word matches in the embeddings.",
        entities: ["Electric Vehicle", "Conductive Charging", "Supply Device", "Safety Requirements"]
      },
      {
        id: "IS 17017 (Part 2) : 2018",
        title: "Electric Vehicle Conductive AC Charging System",
        category: "Electrical",
        summary: "Applies to equipment for the AC charging of electric vehicles with a rated supply voltage up to 1 000 V AC and a rated output voltage up to 1 000 V AC.",
        rationale: "While the query doesn't specify AC or DC, AC charging is the most common form of domestic and commercial EV charging infrastructure. This standard provides crucial specifications for AC systems, making it highly relevant to a general search for EV charging station standards.",
        entities: ["AC Charging", "Voltage Specifications", "Equipment Requirements"]
      },
      {
        id: "IS 6909:1990",
        title: "Supersulphated Cement",
        category: "Civil Engineering",
        summary: "Specifies the requirements for supersulphated cement, which is used in marine works and aggressive water conditions.",
        rationale: "The query specifically asks for cement used in marine works and aggressive water conditions. IS 6909 is the primary standard for supersulphated cement, which is formulated to resist sulphate attack in such environments.",
        entities: ["Supersulphated Cement", "Marine Works", "Aggressive Water", "Sulphate Resistance"]
      },
      {
        id: "IS 269:1989",
        title: "Ordinary Portland Cement, 33 Grade",
        category: "Civil Engineering",
        summary: "Specifies the requirements for 33 grade ordinary Portland cement (OPC 33).",
        rationale: "The query seeks the standard for 33 grade ordinary Portland cement. IS 269 (1989 version) is the definitive standard for this specific grade of cement, covering physical and chemical requirements.",
        entities: ["OPC 33", "Ordinary Portland Cement", "Strength Grade", "Civil Construction"]
      },
      {
        id: "IS 8041",
        title: "Rapid Hardening Portland Cement",
        category: "Civil Engineering",
        summary: "Covers the manufacture and physical/chemical requirements for rapid hardening Portland cement.",
        rationale: "For queries regarding early strength and rapid hardening, IS 8041 is the standard that specifies the accelerated setting and high early strength characteristics required for pre-cast and repair works.",
        entities: ["Rapid Hardening", "Early Strength", "Portland Cement", "Pre-cast Works"]
      }
    ]
  },
  te: {
    title: "AI-ఆధారిత BIS ప్రమాణాల శోధన",
    subtitle: "భారతీయ ప్రమాణాల బ్యూరో కార్పస్‌ను నావిగేట్ చేయడానికి రూపొందించబడిన అత్యంత ఖచ్చితమైన సెమాంటిక్ సెర్చ్ ఇంజన్. స్టేట్-ఆఫ్-ది-ఆర్ట్ వెక్టర్ ఎంబెడ్డింగ్‌లు మరియు జెమిని 1.5 ప్రో రేషనల్ జనరేషన్‌ను ఉపయోగించడం.",
    searchPlaceholder: "BIS ప్రమాణాల కోసం వెతకండి (ఉదా. 'EV ఛార్జింగ్ భద్రత')...",
    identifiedStandards: "గుర్తించబడిన ప్రమాణాలు",
    found: "కనుగొనబడ్డాయి",
    viewDocument: "పత్రాన్ని వీక్షించండి",
    aiRationale: "AI హేతుబద్ధత & వెలికితీత",
    latency: "శోధన సమయం",
    relevance: "సగటు సంబంధం",
    coverage: "టెక్స్ట్ కవరేజ్",
    pipeline: "పైప్‌లైన్ అమలు",
    search: "వెతకండి",
    searchTitle: "సెమాంటిక్ ప్రమాణ శోధన",
    searchDescription: "ఉత్పత్తి వివరణ, వినియోగ సందర్భం లేదా సాంకేతిక ప్రశ్నను నమోదు చేయండి. AI అత్యంత సంబంధిత BIS ప్రమాణాలను గుర్తిస్తుంది.",
    analyzing: "విశ్లేషిస్తోంది",
    exampleQueries: "ఉదాహరణ ప్రశ్నలు:",
    match: "సరిపోలిక",
    distribution: "సెమాంటిక్ సారూప్యత పంపిణీ",
    reasoningTrace: "హేతుబద్ధత ట్రేస్",
    keyEntities: "కీలక సంస్థలు సంగ్రహించబడ్డాయి",
    results: [
      {
        id: "IS 16221 (భాగం 1) : 2015",
        title: "ఎలక్ట్రిక్ వెహికల్ కండక్టివ్ ఛార్జింగ్ సిస్టమ్ పార్ట్ 1 సాధారణ అవసరాలు",
        category: "ఆటోమోటివ్",
        summary: "ఎలక్ట్రిక్ వాహనాల కండక్టివ్ ఛార్జింగ్ కోసం సాధారణ అవసరాలను నిర్దేశిస్తుంది. ఇది సరఫరా పరికరం యొక్క లక్షణాలు మరియు ఆపరేటింగ్ పరిస్థితులను మరియు EVకి కనెక్షన్‌ను కవర్ చేస్తుంది.",
        rationale: "వినియోగదారు ప్రశ్న ప్రత్యేకంగా 'ఛార్జింగ్ స్టేషన్లు' మరియు 'భద్రత' గురించి ప్రస్తావించింది. ఈ ప్రమాణం నేరుగా EV ఛార్జింగ్ కోసం సాధారణ అవసరాలను పరిష్కరిస్తుంది, ఇది ప్రాథమికంగా సరఫరా పరికరం కోసం భద్రతా ప్రోటోకాల్‌లు మరియు కార్యాచరణ పరిస్థితులను కలిగి ఉంటుంది. ఎంబెడ్డింగ్‌లలో ఖచ్చితమైన బహుళ-పదాల సరిపోలికల కారణంగా వెక్టర్ సారూప్యత చాలా ఎక్కువగా ఉంది.",
        entities: ["ఎలక్ట్రిక్ వాహనం", "కండక్టివ్ ఛార్జింగ్", "సరఫరా పరికరం", "భద్రతా అవసరాలు"]
      },
      {
        id: "IS 17017 (భాగం 2) : 2018",
        title: "ఎలక్ట్రిక్ వెహికల్ కండక్టివ్ AC ఛార్జింగ్ సిస్టమ్",
        category: "ఎలక్ట్రికల్",
        summary: "1,000 V AC వరకు రేటెడ్ సప్లై వోల్టేజ్ మరియు 1,000 V AC వరకు రేటెడ్ అవుట్‌పుట్ వోల్టేజ్‌తో ఎలక్ట్రిక్ వాహనాల AC ఛార్జింగ్ కోసం పరికరాలకు వర్తిస్తుంది.",
        rationale: "ప్రశ్న AC లేదా DCని పేర్కొననప్పటికీ, గృహ మరియు వాణిజ్య EV ఛార్జింగ్ అవస్థాపనలో AC ఛార్జింగ్ అత్యంత సాధారణ రూపం. ఈ ప్రమాణం AC సిస్టమ్‌ల కోసం కీలకమైన స్పెసిఫికేషన్‌లను అందిస్తుంది, ఇది EV ఛార్జింగ్ స్టేషన్ ప్రమాణాల కోసం సాధారణ శోధనకు అత్యంత సందర్భోచితంగా ఉంటుంది.",
        entities: ["AC ఛార్జింగ్", "వోల్టేజ్ లక్షణాలు", "పరికరాల అవసరాలు"]
      },
      {
        id: "IS 6909:1990",
        title: "సూపర్ సల్ఫేటెడ్ సిమెంట్",
        category: "సివిల్ ఇంజనీరింగ్",
        summary: "మెరైన్ వర్క్స్ మరియు అగ్రెసివ్ వాటర్ కండిషన్స్‌లో ఉపయోగించే సూపర్ సల్ఫేటెడ్ సిమెంట్ అవసరాలను నిర్దేశిస్తుంది.",
        rationale: "మెరైన్ పనులు మరియు దూకుడు నీటి పరిస్థితులలో ఉపయోగించే సిమెంట్ కోసం ప్రశ్న అడిగారు. IS 6909 అనేది సూపర్ సల్ఫేటెడ్ సిమెంట్ కోసం ప్రాథమిక ప్రమాణం.",
        entities: ["సూపర్ సల్ఫేటెడ్ సిమెంట్", "మెరైన్ పనులు", "సల్ఫేట్ నిరోధకత"]
      },
      {
        id: "IS 269:1989",
        title: "సాధారణ పోర్ట్ ల్యాండ్ సిమెంట్, 33 గ్రేడ్",
        category: "సివిల్ ఇంజనీరింగ్",
        summary: "33 గ్రేడ్ సాధారణ పోర్ట్ ల్యాండ్ సిమెంట్ (OPC 33) కోసం అవసరాలను నిర్దేశిస్తుంది.",
        rationale: "33 గ్రేడ్ సాధారణ పోర్ట్ ల్యాండ్ సిమెంట్ కోసం ప్రమాణాన్ని ప్రశ్న కోరుతోంది. IS 269 (1989 వెర్షన్) ఈ నిర్దిష్ట గ్రేడ్ సిమెంట్ కోసం ఖచ్చితమైన ప్రమాణం.",
        entities: ["OPC 33", "సాధారణ పోర్ట్ ల్యాండ్ సిమెంట్", "గ్రేడ్"]
      },
      {
        id: "IS 8041",
        title: "రాపిడ్ హార్డెనింగ్ పోర్ట్ ల్యాండ్ సిమెంట్",
        category: "సివిల్ ఇంజనీరింగ్",
        summary: "రాపిడ్ హార్డెనింగ్ పోర్ట్ ల్యాండ్ సిమెంట్ తయారీ మరియు భౌతిక/రసాయన అవసరాలను కవర్ చేస్తుంది.",
        rationale: "ప్రారంభ బలం మరియు వేగవంతమైన గట్టిపడటం గురించి ప్రశ్నల కోసం, IS 8041 అనేది వేగవంతమైన సెట్టింగ్ మరియు అధిక ప్రారంభ బలాన్ని నిర్దేశించే ప్రమాణం.",
        entities: ["రాపిడ్ హార్డెనింగ్", "ప్రారంభ బలం", "పోర్ట్ ల్యాండ్ సిమెంట్"]
      }
    ]
  },
  hi: {
    title: "AI-संचालित BIS मानक खोज",
    subtitle: "भारतीय मानक ब्यूरो कॉर्पस को नेविगेट करने के लिए डिज़ाइन किया गया एक अत्यधिक सटीक शब्दार्थ खोज इंजन। अत्याधुनिक वेक्टर एम्बेडिंग और जेमिनी 1.5 प्रो तर्क पीढ़ी का उपयोग करना।",
    searchPlaceholder: "BIS मानकों के लिए खोजें (जैसे 'EV चार्जिंग सुरक्षा')...",
    identifiedStandards: "पहचाने गए मानक",
    found: "मिले",
    viewDocument: "दस्तावेज़ देखें",
    aiRationale: "AI तर्क और निष्कर्षण",
    latency: "खोज विलंबता",
    relevance: "औसत प्रासंगिकता",
    coverage: "टेक्स्ट कवरेज",
    pipeline: "पाइपलाइन निष्पादन",
    search: "खोजें",
    searchTitle: "सिमेंटिक मानक खोज",
    searchDescription: "उत्पाद विवरण, उपयोग मामला या तकनीकी प्रश्न दर्ज करें। AI सबसे प्रासंगिक BIS मानकों की पहचान करेगा।",
    analyzing: "विश्लेषण कर रहा है",
    exampleQueries: "उदाहरण प्रश्न:",
    match: "मिलान",
    distribution: "सिमेंटिक समानता वितरण",
    reasoningTrace: "तर्क ट्रेस",
    keyEntities: "निकालने गए प्रमुख निकाय",
    results: [
      {
        id: "IS 16221 (भाग 1) : 2015",
        title: "इलेक्ट्रिक वाहन कंडक्टिव चार्जिंग सिस्टम पार्ट 1 सामान्य आवश्यकताएं",
        category: "ऑटोमोटिव",
        summary: "इलेक्ट्रिक वाहनों की कंडक्टिव चार्जिंग के लिए सामान्य आवश्यकताओं को निर्दिष्ट करता है। यह आपूर्ति उपकरण की विशेषताओं और परिचालन स्थितियों और ईवी के कनेक्शन को कवर करता है।",
        rationale: "उपयोगकर्ता प्रश्न विशेष रूप से 'चार्जिंग स्टेशन' और 'सुरक्षा' का उल्लेख करता है। यह मानक सीधे ईवी चार्जिंग के लिए सामान्य आवश्यकताओं को संबोधित करता है, जो मौलिक रूप से आपूर्ति उपकरण के लिए सुरक्षा प्रोटोकॉल और परिचालन स्थितियों को शामिल करता है। एम्बेडिंग में सटीक बहु-शब्द मिलान के कारण वेक्टर समानता असाधारण रूप से उच्च है।",
        entities: ["इलेक्ट्रिक वाहन", "कंडक्टिव चार्जिंग", "आपूर्ति उपकरण", "सुरक्षा आवश्यकताएं"]
      },
      {
        id: "IS 17017 (भाग 2) : 2018",
        title: "इलेक्ट्रिक वाहन कंडक्टिव एसी चार्जिंग सिस्टम",
        category: "इलेक्ट्रिकल",
        summary: "1,000 V AC तक रेटेड आपूर्ति वोल्टेज और 1,000 V AC तक रेटेड आउटपुट वोल्टेज वाले इलेक्ट्रिक वाहनों की AC चार्जिंग के लिए उपकरणों पर लागू होता है।",
        rationale: "जबकि प्रश्न एसी या डीसी निर्दिष्ट नहीं करता है, घरेलू और वाणिज्यिक ईवी चार्जिंग बुनियादी ढांचे में एसी चार्जिंग सबसे आम रूप है। यह मानक एसी सिस्टम के लिए महत्वपूर्ण विनिर्देश प्रदान करता है, जो इसे ईवी चार्जिंग स्टेशन मानकों की सामान्य खोज के लिए अत्यधिक प्रासंगिक बनाता है।",
        entities: ["एसी चार्जिंग", "वोल्टेज विनिर्देश", "उपकरण आवश्यकताएं"]
      },
      {
        id: "IS 6909:1990",
        title: "सुपरसल्फेट सीमेंट",
        category: "सिविल इंजीनियरिंग",
        summary: "सुपरसल्फेट सीमेंट की आवश्यकताओं को निर्दिष्ट करता है, जिसका उपयोग समुद्री कार्यों और आक्रामक जल स्थितियों में किया जाता है।",
        rationale: "प्रश्न विशेष रूप से समुद्री कार्यों और आक्रामक जल स्थितियों में उपयोग किए जाने वाले सीमेंट के बारे में पूछता है। IS 6909 सुपरसल्फेट सीमेंट के लिए प्राथमिक मानक है।",
        entities: ["सुपरसल्फेट सीमेंट", "समुद्री कार्य", "सल्फेट प्रतिरोध"]
      },
      {
        id: "IS 269:1989",
        title: "साधारण पोर्टलैंड सीमेंट, 33 ग्रेड",
        category: "सिविल इंजीनियरिंग",
        summary: "33 ग्रेड साधारण पोर्टलैंड सीमेंट (OPC 33) की आवश्यकताओं को निर्दिष्ट करता है।",
        rationale: "प्रश्न 33 ग्रेड साधारण पोर्टलैंड सीमेंट के लिए मानक चाहता है। IS 269 (1989 संस्करण) सीमेंट के इस विशिष्ट ग्रेड के लिए निश्चित मानक है।",
        entities: ["OPC 33", "साधारण पोर्टलैंड सीमेंट", "ग्रेड"]
      },
      {
        id: "IS 8041",
        title: "रैपिड हार्डनिंग पोर्टलैंड सीमेंट",
        category: "सिविल इंजीनियरिंग",
        summary: "रैपिड हार्डनिंग पोर्टलैंड सीमेंट के निर्माण और भौतिक/रासायनिक आवश्यकताओं को कवर करता है।",
        rationale: "प्रारंभिक शक्ति और तेजी से सख्त होने के संबंध में प्रश्नों के लिए, IS 8041 वह मानक है जो आवश्यक त्वरित सेटिंग विशेषताओं को निर्दिष्ट करता है।",
        entities: ["रैपिड हार्डनिंग", "प्रारंभिक शक्ति", "पोर्टलैंड सीमेंट"]
      }
    ]
  }
};
