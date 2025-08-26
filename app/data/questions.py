# app/data/questions.py

# Categories (labels)
CATEGORY_LABELS = {
    "logic":   {"mr": "तर्कशक्ती व समस्या सोडवणे", "en": "Logic & Problem Solving"},
    "arts":    {"mr": "कला व सर्जनशीलता",          "en": "Arts & Creativity"},
    "science": {"mr": "विज्ञान व प्रयोग",           "en": "Science & Experiments"},
    "social":  {"mr": "सामाजिक व नेतृत्व",         "en": "Social & Leadership"},
    "commerce":{"mr": "व्यवसाय व व्यवहारिक",       "en": "Commerce & Practical Skills"},
}

# Field mapping (Top recommendations)
FIELD_MAP = {
    "logic": {
        "en": ["Engineering (CS/Mechanical/Electrical/Civil)", "Data & Coding", "Math-intensive careers"],
        "mr": ["अभियांत्रिकी (CS/मेch/इलेक्ट्रिकल/सिव्हिल)", "डेटा व कोडिंग", "गणिताधिष्ठित करिअर"]
    },
    "arts": {
        "en": ["Fine Arts & Design", "Performing Arts (Music/Dance/Drama)", "Digital Arts (Graphics/Video/Animation)"],
        "mr": ["फाइन आर्ट्स व डिझाइन", "परफॉर्मिंग आर्ट्स (संगीत/नृत्य/नाटक)", "डिजिटल आर्ट (ग्राफिक्स/व्हिडिओ/अॅनिमेशन)"]
    },
    "science": {
        "en": ["Medical & Health", "Pure Sciences (Physics/Chem/Bio)", "Space & Robotics", "Environmental Science"],
        "mr": ["मेडिकल व हेल्थ", "शुद्ध विज्ञान (भौतिक/रसायन/जीव)", "अंतराळ व रोबोटिक्स", "पर्यावरण विज्ञान"]
    },
    "social": {
        "en": ["Civil Services", "Teaching & Training", "Psychology & Counseling", "NGO/Social Work"],
        "mr": ["सिव्हिल सर्व्हिसेस", "शिक्षण/ट्रेनिंग", "समुपदेशन/सायकोलॉजी", "NGO/सामाजिक कार्य"]
    },
    "commerce": {
        "en": ["Finance/Banking/Accounts", "Business & Entrepreneurship", "Marketing & Sales", "Management"],
        "mr": ["फायनान्स/बँकिंग/अकाऊंट्स", "बिझनेस व उद्योजकता", "मार्केटिंग व सेल्स", "मॅनेजमेंट"]
    }
}

# Helper: short option sets
LIKERT_5 = [
    {"label": "Strongly Agree / पूर्ण सहमत", "value": 5},
    {"label": "Agree / सहमत",               "value": 4},
    {"label": "Not Sure / खात्री नाही",      "value": 3},
    {"label": "Disagree / असहमत",           "value": 2},
    {"label": "Strongly Disagree / अजिबात सहमत नाही", "value": 1},
]

EMOJI_4 = [
    {"label": "😞", "value": 1},
    {"label": "😐", "value": 2},
    {"label": "🙂", "value": 3},
    {"label": "😍", "value": 4},
]

# 50 Questions — each has: id, category, mr, en, type
QUESTIONS = [
    # ---------- LOGIC (1-10)
    *[
        {"id": i, "category": "logic", "type": "likert", "options": LIKERT_5,
         "mr": mr, "en": en}
        for i, (mr, en) in enumerate([
            ("तुला गणिताचे कठीण प्रश्न सोडवायला आवडतात का?", "Do you enjoy solving difficult math problems?"),
            ("तुला पझल्स, Sudoku किंवा riddles सोडवायला आवडतात का?", "Do you like solving puzzles, Sudoku, or riddles?"),
            ("तुला problem सोडवताना वेगवेगळे solutions शोधायला आवडते का?", "Do you enjoy finding multiple solutions to a problem?"),
            ("तुला computer coding/logic games मध्ये रस आहे का?", "Are you interested in computer coding/logic games?"),
            ("तुला reasoning questions (series/patterns) सोडवायला आवडतात का?", "Do you like solving reasoning questions (series, patterns)?"),
            ("तुला एखादी गोष्ट logically explain करायला सोप्पं जातं का?", "Do you find it easy to explain things logically?"),
        ], start=1)
    ],
    {"id": 7, "category": "logic", "type": "emoji", "options": EMOJI_4,
     "mr": "तुला गणित/विज्ञानात numbers वापरायला मजा येते का?",
     "en": "Do you enjoy working with numbers in math or science?"},
    {"id": 8, "category": "logic", "type": "slider", "slider_min": 0, "slider_max": 10,
     "mr": "तुला steps follow करून experiments plan करायला आवडते का?",
     "en": "Do you like planning step-by-step experiments?"},
    {"id": 9, "category": "logic", "type": "multi",
     "multi_options": ["Aptitude questions सोप्पे वाटतात", "Series/Patterns पटकन कळतात", "Time-bound problems आवडतात", "लांब calculation comfortable"],
     "mr": "खालीलपैकी कोणत्या गोष्टी तुझ्यावर लागू पडतात? (एकाहून अधिक निवडू शकतोस)",
     "en": "Which of the following apply to you? (You can select multiple)"},
    {"id": 10, "category": "logic", "type": "slider", "slider_min": 0, "slider_max": 10,
     "mr": "तुला एखादी नवीन समस्या आली तर ती creative पद्धतीने सोडवायला किती आवडतं?",
     "en": "When faced with a new problem, how much do you enjoy solving it creatively?"},

    # ---------- ARTS (11-20)
    *[
        {"id": i, "category": "arts", "type": "likert", "options": LIKERT_5,
         "mr": mr, "en": en}
        for i, (mr, en) in enumerate([
            ("तुला drawing/painting/sketching करायला आवडते का?", "Do you enjoy drawing, painting, or sketching?"),
            ("तुला stories लिहायला किंवा poems compose करायला आवडते का?", "Do you like writing stories or composing poems?"),
            ("तुला नाटक/अभिनय/stage performance मध्ये रस आहे का?", "Are you interested in acting, drama or stage performance?"),
            ("तुला गाणं म्हणणं किंवा वाद्य वाजवणं आवडतं का?", "Do you like singing or playing musical instruments?"),
            ("तुला photography/video making मध्ये रस आहे का?", "Are you interested in photography or video making?"),
            ("तुला fashion/decorations करण्याची आवड आहे का?", "Do you enjoy fashion designing or decorations?"),
        ], start=11)
    ],
    {"id": 17, "category": "arts", "type": "emoji", "options": EMOJI_4,
     "mr": "तुला creative काम केल्यावर उत्साह वाढतो का?", "en": "Do you feel energized after creative work?"},
    {"id": 18, "category": "arts", "type": "slider", "slider_min": 0, "slider_max": 10,
     "mr": "तुला digital art/graphic design शिकण्यात किती उत्सुकता आहे?",
     "en": "How eager are you to learn digital art/graphic design?"},
    {"id": 19, "category": "arts", "type": "multi",
     "multi_options": ["Doodling habit आहे", "Theme decoration करायला आवडतं", "Photo/Video editing जमते", "Colours/Styles कडे लक्ष असतं"],
     "mr": "खालीलपैकी काय काय तुझ्याकडे आहे/आवडतं? (Multiple)",
     "en": "Which of these do you do/like? (Multiple)"},
    {"id": 20, "category": "arts", "type": "slider", "slider_min": 0, "slider_max": 10,
     "mr": "तुला नवीन art forms (music/dance/visual) try करायला किती आवडतं?",
     "en": "How much do you enjoy trying new art forms (music/dance/visual)?"},

    # ---------- SCIENCE (21-30)
    *[
        {"id": i, "category": "science", "type": "likert", "options": LIKERT_5,
         "mr": mr, "en": en}
        for i, (mr, en) in enumerate([
            ("तुला lab experiments करायला आवडतात का?", "Do you enjoy doing lab experiments?"),
            ("तुला machines/gadgets कसे काम करतात समजून घ्यायला आवडते का?", "Do you like understanding how machines/gadgets work?"),
            ("तुला biology मधील human body/निसर्ग बद्दल जिज्ञासा वाटते का?", "Are you curious about human body or nature in biology?"),
            ("तुला physics experiments (light/magnetism) आवडतात का?", "Do you like physics experiments (light/magnetism)?"),
            ("तुला doctor/scientist/engineer professions मध्ये रस आहे का?", "Are you interested in doctor/scientist/engineer careers?"),
            ("तुला environment study व संरक्षण आवडतं का?", "Do you like environment study and protection?"),
        ], start=21)
    ],
    {"id": 27, "category": "science", "type": "emoji", "options": EMOJI_4,
     "mr": "तुला space/astronomy ची कल्पना thrill देते का?", "en": "Does space/astronomy thrill you?"},
    {"id": 28, "category": "science", "type": "slider", "slider_min": 0, "slider_max": 10,
     "mr": "machines उघडून/repair करून बघण्याची इच्छा किती?", "en": "How much do you want to open/repair machines?"},
    {"id": 29, "category": "science", "type": "multi",
     "multi_options": ["Science videos/experiments बघतो", "DIY kits try करतो", "Science fairs मध्ये भाग घेतो", "New discoveries वाचतो"],
     "mr": "खालीलपैकी काय काय करतोस? (Multiple)", "en": "Which of these do you do? (Multiple)"},
    {"id": 30, "category": "science", "type": "slider", "slider_min": 0, "slider_max": 10,
     "mr": "तुला नवीन वैज्ञानिक शोधांबद्दल वाचण्यात किती रस आहे?",
     "en": "How interested are you in reading about new scientific discoveries?"},

    # ---------- SOCIAL (31-40)
    *[
        {"id": i, "category": "social", "type": "likert", "options": LIKERT_5,
         "mr": mr, "en": en}
        for i, (mr, en) in enumerate([
            ("तुला लोकांना मदत करायला आवडते का?", "Do you like helping people?"),
            ("तुला group मध्ये काम करायला आवडतं का?", "Do you enjoy working in groups?"),
            ("तुला leader बनून जबाबदारी घ्यायला आवडते का?", "Do you like taking responsibility as a leader?"),
            ("तुला लोकांशी बोलून/समजावून पटवून द्यायला आवडते का?", "Do you enjoy convincing people?"),
            ("तुला friends/family मधल्या समस्या सोडवायला आवडते का?", "Do you like solving problems of friends/family?"),
            ("तुला सामाजिक उपक्रम (स्वच्छता/charity) आवडतात का?", "Are you interested in social activities (cleanliness/charity)?"),
        ], start=31)
    ],
    {"id": 37, "category": "social", "type": "emoji", "options": EMOJI_4,
     "mr": "stage वर बोलताना कसं वाटतं?", "en": "How do you feel about speaking on stage?"},
    {"id": 38, "category": "social", "type": "slider", "slider_min": 0, "slider_max": 10,
     "mr": "समाज/राजकारण विषयांवर चर्चा करायची इच्छा किती?", "en": "How much do you like discussing social/political topics?"},
    {"id": 39, "category": "social", "type": "multi",
     "multi_options": ["Friends ना motivate करतो", "Team events आयोजित करतो", "Debates मध्ये भाग घेतो", "Volunteer करतो"],
     "mr": "खालीलपैकी काय काय करतोस? (Multiple)", "en": "Which of these do you do? (Multiple)"},
    {"id": 40, "category": "social", "type": "slider", "slider_min": 0, "slider_max": 10,
     "mr": "तुला लोकांसोबत नवीन उपक्रम सुरू करायला किती आवडतं?",
     "en": "How much do you enjoy starting new initiatives with people?"},

    # ---------- COMMERCE (41-50)
    *[
        {"id": i, "category": "commerce", "type": "likert", "options": LIKERT_5,
         "mr": mr, "en": en}
        for i, (mr, en) in enumerate([
            ("तुला पैशांचे management करायला आवडते का?", "Do you like managing money?"),
            ("तुला छोट्या गोष्टी विकणे/trade करणे आवडते का?", "Do you like selling small items or trading?"),
            ("तुला accounts/balance maintain करायला सोप्पं वाटतं का?", "Do you find it easy to maintain accounts/balance?"),
            ("तुला business ideas विचारायला आवडतं का?", "Do you like thinking about business ideas?"),
            ("तुला economics/finance बद्दल कुतूहल आहे का?", "Are you curious about economics/finance?"),
            ("तुला marketing/advertisement मध्ये रस आहे का?", "Are you interested in marketing/advertising?"),
        ], start=41)
    ],
    {"id": 47, "category": "commerce", "type": "emoji", "options": EMOJI_4,
     "mr": "खर्च/बचत पाहताना कसं वाटतं?", "en": "How do you feel about tracking cost/savings?"},
    {"id": 48, "category": "commerce", "type": "slider", "slider_min": 0, "slider_max": 10,
     "mr": "छोटा business चालवण्याची इच्छा किती?", "en": "How much do you want to run a small business?"},
    {"id": 49, "category": "commerce", "type": "multi",
     "multi_options": ["Market survey करतो", "लोकांचे opinion गोळा करतो", "Sales pitch try करतो", "Budget बनवतो"],
     "mr": "खालीलपैकी काय काय करतोस? (Multiple)", "en": "Which of these do you do? (Multiple)"},
    {"id": 50, "category": "commerce", "type": "slider", "slider_min": 0, "slider_max": 10,
     "mr": "तुला भविष्यात मोठ्या कंपनीत काम करण्यापेक्षा स्वतःचा business चालवण्यात किती रस आहे?",
     "en": "How much are you interested in running your own business instead of working in a big company?"},
]
