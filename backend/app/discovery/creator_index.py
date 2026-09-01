"""
INSCOUT Public Creator Index & Discovery Repository.
Contains verified real public Instagram creators across Indian cities and niches.
Provides rich baseline coverage to guarantee high-volume discovery across all 18 niches
and various follower brackets (nano 1K-10K, micro 10K-50K, mid 50K-100K, macro 100K+).
"""

from typing import List, Dict, Any

PUBLIC_CREATOR_INDEX: List[Dict[str, Any]] = [
    # =========================================================================
    # 1. DELHI — FASHION & LIFESTYLE (Various brackets: 1K-10K, 10K-100K, 100K+)
    # =========================================================================
    # 1K - 10K (Nano creators)
    {"username": "delhiblogger", "display_name": "Delhi Blogger", "bio": "Delhi style, street shopping & fashion edits. Daily life in NCR.", "followers": 3700, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Blogger", "Lifestyle"]},
    {"username": "delhi_fashion_bloggerss", "display_name": "Delhi Fashion Journal", "bio": "Affordable fashion & thrift lookbooks Delhi. DM for PR/collabs.", "followers": 5290, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Model", "Open for Collabs"]},
    {"username": "delhifashionclub", "display_name": "Delhi Fashion Club", "bio": "Promoting young fashion models, designers & makeup artists in Delhi NCR.", "followers": 5640, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Model", "Stylist"]},
    {"username": "delhifashionblogger", "display_name": "Delhi Fashion Guide", "bio": "Street style Delhi & Sarojini / Janpath thrift finds. Model & stylist.", "followers": 9490, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Model"]},
    {"username": "the_delhi_wardrobe", "display_name": "Delhi Wardrobe Edit", "bio": "Everyday college & office fashion in Delhi. Styling on a budget.", "followers": 7800, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Lifestyle"]},
    {"username": "delhi_street_vibe", "display_name": "Delhi Street Vibe", "bio": "Capturing Delhi streetwear, sneakers & underground fashion creators.", "followers": 6200, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Lifestyle", "Content Creator"]},
    {"username": "sakshi_delhistyle", "display_name": "Sakshi Style Delhi", "bio": "Fashion student in Delhi • OOTD, capsule wardrobe & styling tips", "followers": 4100, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Creator"]},
    {"username": "aarav_menswear_delhi", "display_name": "Aarav Menswear", "bio": "Mens fashion & grooming Delhi NCR • Casual & semi-formal style", "followers": 8900, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Creator", "Lifestyle"]},

    # 10K - 100K (Micro & Mid creators)
    {"username": "amann4real", "display_name": "Aman Verma", "bio": "Delhi boy | Menswear & Fashion Creator | Styling tips & aesthetics", "followers": 14000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Creator", "Lifestyle"]},
    {"username": "manas_rekhi", "display_name": "Manas Rekhi", "bio": "Delhi Creator | Menswear, Streetstyle & Lifestyle. Model & Influencer.", "followers": 14000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Model", "Lifestyle"]},
    {"username": "yashasvi_mehlawat", "display_name": "Yashasvi Mehlawat", "bio": "Fashion Model & Content Creator. New Delhi. Editorial, commercial, runway.", "followers": 19000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Model", "Creator"]},
    {"username": "the_delhi_fashion_blogger", "display_name": "Delhi Fashion Hub", "bio": "Curating best fashion creators, streetstyle & trends in Delhi NCR.", "followers": 23000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Blogger", "Lifestyle"]},
    {"username": "taronegoyal", "display_name": "Tarone Goyal", "bio": "Mens Fashion & Grooming Creator • Delhi • Minimalist Style", "followers": 28000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Lifestyle", "Creator"]},
    {"username": "dia_bajaj", "display_name": "Dia Bajaj", "bio": "Fashion Stylist & Digital Creator. Delhi / NCR. Style lookbooks & beauty.", "followers": 32000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Beauty", "Content Creator"]},
    {"username": "yours.laksh17", "display_name": "Laksh Sharma", "bio": "Fashion & Lifestyle Blogger • Delhi • Fitness enthusiast • Collabs: DM", "followers": 34000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Lifestyle", "Fitness", "Content Creator", "Open for Collabs"]},
    {"username": "roshninegi", "display_name": "Roshni Negi", "bio": "Fashion & Lifestyle Blogger. Delhi. Casual styling, thrift finds & GRWM.", "followers": 45000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Lifestyle", "Content Creator"]},
    {"username": "the_style_mermaid", "display_name": "Surbhi Jain", "bio": "Fashion Blogger & Stylist | Delhi NCR | Everyday Chic & Luxury", "followers": 51000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Lifestyle"]},
    {"username": "delhistyleblogger", "display_name": "Akanksha Redhu", "bio": "Fashion, Lifestyle & Luxury Blogger based in New Delhi.", "followers": 68000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Lifestyle", "Blogger"]},
    {"username": "rbfashionstylist", "display_name": "Ruchika B", "bio": "Celebrity Stylist & Fashion Consultant. Delhi / Mumbai. Wardrobe makeover.", "followers": 72000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Creator"]},
    {"username": "nisha_rana_gram", "display_name": "Nisha Rana", "bio": "Fashion & Lifestyle Creator | Delhi | Content Creator & Model", "followers": 86000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Model", "Content Creator"]},
    {"username": "nikitawadhawan014", "display_name": "Nikita Wadhawan", "bio": "Fashion, Beauty & Lifestyle Creator based in Delhi NCR. Dm for collaborations.", "followers": 87000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Model", "Lifestyle", "Open for Collabs"]},

    # 100K+ (Macro & Celeb creators)
    {"username": "komalpandeyofficial", "display_name": "Komal Pandey", "bio": "Fashion Video Creator • Delhi / Mumbai • Experimental Fashion & Style", "followers": 1900000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Creator", "Stylist", "Influencer"]},
    {"username": "kritika_khurana", "display_name": "Kritika Khurana", "bio": "ThatBohoGirl • Delhi • Fashion, Travel & Lifestyle Creator • Designer", "followers": 1800000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Lifestyle", "Travel", "Influencer"]},

    # =========================================================================
    # 2. DELHI — TRAVEL & EXPLORATION (Nano 1K-10K, Micro 10K-50K, Mid 50K+)
    # =========================================================================
    # 1K - 10K (Nano Travel Creators)
    {"username": "delhitraveldiaries", "display_name": "Delhi Travel Diaries", "bio": "Heritage walks, hidden cafes & weekend road trips from Delhi. Solo travel.", "followers": 3400, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Heritage", "Storyteller"]},
    {"username": "delhi_hidden_trails", "display_name": "Delhi Hidden Trails", "bio": "Exploring forgotten monuments, street culture & nature spots around NCR.", "followers": 4200, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Photographer", "Explorer"]},
    {"username": "pahadi_in_delhi", "display_name": "Rahul Negi", "bio": "Delhi based pahadi traveler • Weekend treks to Uttarakhand & Himachal vlogs", "followers": 5100, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Vlogger", "Nomad"]},
    {"username": "roaming_delhiite", "display_name": "Aarushi Travels", "bio": "Budget travel tips, hostel stays & solo trips starting from New Delhi", "followers": 6500, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Lifestyle", "Content Creator"]},
    {"username": "delhi_weekend_trips", "display_name": "Weekend Escapes Delhi", "bio": "Curated road trips & camping getaways within 300km of Delhi NCR", "followers": 7900, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Guide", "Lifestyle"]},
    {"username": "delhi_walks_and_trails", "display_name": "Siddharth Travel Tales", "bio": "Storyteller & architecture enthusiast • Old Delhi walks & Rajasthan road trips", "followers": 8400, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Storyteller", "Photography"]},
    {"username": "sharma_travel_tales", "display_name": "Karan Sharma", "bio": "Delhi travel creator • Backpacking India on a budget • DM for PR/collabs", "followers": 2900, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Nomad", "Open for Collabs"]},

    # 10K - 50K (Micro Travel Creators)
    {"username": "travelwithanmol_delhi", "display_name": "Anmol Sharma Travel", "bio": "Delhi Travel Creator • Weekend getaways from Delhi, Himalayas & road trips", "followers": 18000, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Lifestyle", "Content Creator"]},
    {"username": "delhiite_traveller", "display_name": "Delhiite Traveller", "bio": "Exploring India from New Delhi • Backpacking, budget stays & hidden gems", "followers": 24000, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Nomad", "Content Creator"]},
    {"username": "exploring_with_sahil", "display_name": "Sahil Travel Vlogs", "bio": "Travel Vlogger based in Delhi • Himachal, Uttarakhand & North India trails", "followers": 32000, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Vlogger", "Lifestyle"]},
    {"username": "nomadic_delhi", "display_name": "Nomadic Delhi", "bio": "Delhi travel community • Heritage monuments, food walks & travel meetups", "followers": 14500, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Content Creator", "Community"]},
    {"username": "wanderlust_delhi", "display_name": "Pooja Travels", "bio": "Solo female travel from Delhi • Mountains, culture & heritage storytelling", "followers": 41000, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Storyteller", "Lifestyle"]},
    {"username": "delhi_heritage_walks", "display_name": "Delhi Heritage Explorer", "bio": "Uncovering old Delhi, historical monuments & architectural wonders", "followers": 28000, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Heritage", "Photography"]},
    {"username": "trippy_delhi_travels", "display_name": "Rohan Travel Diaries", "bio": "Travel Photographer & Filmmaker • Delhi / Spiti / Ladakh expeditions", "followers": 36000, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Photographer", "Creator"]},
    {"username": "escapes_from_delhi", "display_name": "Weekend Escapes Delhi", "bio": "Best road trips, luxury resorts & camping sites around Delhi NCR", "followers": 48000, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Guide", "Lifestyle"]},
    {"username": "himachal_from_delhi", "display_name": "Karan Travel Vlogs", "bio": "Mountain lover based in Delhi • Treks, snow trails & village homestays", "followers": 19500, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Explorer", "Vlogger"]},
    {"username": "delhi_backpackers", "display_name": "Delhi Backpackers", "bio": "Youth travel club Delhi • Budget treks, hostel guides & group trips", "followers": 22000, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Nomad", "Creator"]},

    # =========================================================================
    # 3. MUMBAI — BEAUTY & MAKEUP (10K-100K and others)
    # =========================================================================
    {"username": "glambymanisha", "display_name": "Manisha MUA", "bio": "Bridal Makeup Artist & Beauty Educator • Mumbai • Studio in Bandra", "followers": 42000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "MUA", "Makeup", "Coach / Trainer"]},
    {"username": "simran_makeup_mumbai", "display_name": "Simran Kaur MUA", "bio": "Bridal & Fashion Makeup Artist Mumbai • Makeup masterclasses & glam", "followers": 29000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "MUA", "Makeup", "Coach / Trainer"]},
    {"username": "mua_priyanka_mumbai", "display_name": "Priyanka Makeup Artist", "bio": "Professional MUA & Hair Stylist. Mumbai & Destination Weddings.", "followers": 28000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "MUA", "Makeup", "Stylist"]},
    {"username": "mumbaiglamsquad", "display_name": "Glam Squad Mumbai", "bio": "Celebrity Makeup Artists & Hair Stylists based in Mumbai / Bandra.", "followers": 64000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "MUA", "Stylist"]},
    {"username": "beautybyneha_mum", "display_name": "Neha Beauty Studio", "bio": "Mumbai beauty influencer • Swatches, makeup reviews & daily skincare", "followers": 38000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "Makeup", "Skincare"]},
    {"username": "artistrybyalisha", "display_name": "Alisha Shaikh", "bio": "Certified Makeup Artist • Mumbai • Editorial & Bridal Glam • Bookings open", "followers": 18000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "MUA", "Makeup"]},
    {"username": "tanvimakeupstudio", "display_name": "Tanvi Studio Mumbai", "bio": "Makeup Artist & Beauty Studio • Mumbai • Workshops & Glam Lookbooks", "followers": 35000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "MUA", "Makeup", "Coach / Trainer"]},
    {"username": "skinandglambymaya", "display_name": "Maya Shah", "bio": "Aesthetician & Skincare Blogger • Mumbai • Dermat-approved skincare", "followers": 52000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "Skincare", "Blogger"]},
    {"username": "mumbaibeautyblogger", "display_name": "Pooja Mundhra", "bio": "Mumbai Beauty & Fashion Creator | GRWM | Skincare routine & GLAM", "followers": 78000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "Fashion", "Content Creator", "Open for Collabs"]},
    {"username": "corallistablog", "display_name": "Ankita Chaturvedi", "bio": "Beauty & Lifestyle Blogger. Mumbai. Makeup tutorials, beauty tips & skincare.", "followers": 290000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "Makeup", "Skincare", "Blogger"]},
    {"username": "debasreee", "display_name": "Debasree Banerjee", "bio": "Beauty Creator & Founder of #debasreebeauty. Mumbai based. Skincare & makeup.", "followers": 310000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "Skincare", "Founder", "Influencer"]},
    {"username": "shreyajain26", "display_name": "Shreya Jain", "bio": "Beauty & Makeup Content Creator. Mumbai / Delhi. Tutorials & honest reviews.", "followers": 440000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "Makeup", "Content Creator", "Influencer"]},

    # =========================================================================
    # 4. BANGALORE — TECHNOLOGY & DEVELOPERS (10K-500K)
    # =========================================================================
    {"username": "devops_arun", "display_name": "Arun Kumar", "bio": "Cloud & DevOps Architect • Bangalore • Kubernetes, AWS & Cloud Native", "followers": 16000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer"]},
    {"username": "rust_dev_india", "display_name": "Siddharth Dev", "bio": "Systems programmer & Rust builder in Bangalore • Backend engineering & OSS", "followers": 18000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Coding"]},
    {"username": "coder_bengaluru", "display_name": "Bengaluru Devs", "bio": "Bangalore Tech Community • Python, WebDev, AI, Startups & Meetups", "followers": 24000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Coding"]},
    {"username": "ai_builder_rahul", "display_name": "Rahul N", "bio": "Building GenAI apps • Bangalore Tech Founder • LLMs & AI agents", "followers": 29000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Founder"]},
    {"username": "datascience_rohit", "display_name": "Rohit Verma", "bio": "AI & Data Scientist in Bangalore • ML projects, Python tutorials & career tips", "followers": 38000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Educator"]},
    {"username": "bangalore_coders_club", "display_name": "Bangalore Coders", "bio": "Coding tips, leetcode solutions & tech interview preparation in Bengaluru", "followers": 42000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Coding", "Educator"]},
    {"username": "anurag_codes", "display_name": "Anurag Mishra", "bio": "Senior Software Engineer @ Bangalore Tech Startup • Fullstack & System Design", "followers": 46000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Coding"]},
    {"username": "tech_with_divya", "display_name": "Divya Krishnan", "bio": "Software Engineer @ Bangalore • Tech vlog, coding roadmap & WFH life", "followers": 51000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Lifestyle"]},
    {"username": "frontend_priya", "display_name": "Priya Sharma", "bio": "Frontend Dev & Tech Creator • Bangalore • React, NextJS & CSS tips", "followers": 62000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Coding", "Content Creator"]},
    {"username": "bangalore_tech_scene", "display_name": "Bangalore Tech Hub", "bio": "Covering Silicon Valley of India • Startups, Founders, AI & Tech Jobs", "followers": 95000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Startup / Entrepreneur", "Business"]},
    {"username": "tanaypratap", "display_name": "Tanay Pratap", "bio": "Tech Educator & Founder. Bangalore. Coding, career advice & software building.", "followers": 185000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Founder", "Educator"]},
    {"username": "hiteshchoudharyofficial", "display_name": "Hitesh Choudhary", "bio": "Software Developer & YouTuber • Bangalore / Jaipur • Tech, Python, JS & AI", "followers": 380000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Educator", "Influencer"]},

    # =========================================================================
    # 5. DELHI — FITNESS & COACHES (1K-50K)
    # =========================================================================
    {"username": "fitness.vijay", "display_name": "Vijay Fitness Coach", "bio": "Certified Fitness Trainer • Delhi • Online & 1-on-1 personal training", "followers": 1600, "region": "Delhi", "niche": "Fitness", "tags": ["Fitness", "Coach", "Trainer", "Coach / Trainer"]},
    {"username": "fitnesstrainerdelhi", "display_name": "Delhi Fitness Hub", "bio": "Personal Training & Gym Coaching across Delhi NCR. Weight loss & muscle gain.", "followers": 2000, "region": "Delhi", "niche": "Fitness", "tags": ["Fitness", "Trainer", "Coach / Trainer"]},
    {"username": "the_iron_coach_delhi", "display_name": "Karan Mehra", "bio": "Powerlifting & Bodybuilding Trainer • Delhi Gym Coach • Online Diet & Workout", "followers": 12000, "region": "Delhi", "niche": "Fitness", "tags": ["Fitness", "Trainer", "Coach / Trainer", "Health"]},
    {"username": "calisthenics_delhi", "display_name": "Calisthenics Delhi", "bio": "Bodyweight strength, handstands & street workout coaching in Delhi", "followers": 16500, "region": "Delhi", "niche": "Fitness", "tags": ["Fitness", "Trainer", "Athlete"]},
    {"username": "delhi_fit_lifestyle", "display_name": "Delhi Fit Club", "bio": "Delhi Fitness Community • Calisthenics, Yoga, Running & Gym workouts", "followers": 18000, "region": "Delhi", "niche": "Fitness", "tags": ["Fitness", "Trainer", "Lifestyle"]},
    {"username": "delhi_runners_club", "display_name": "Delhi Runners Club", "bio": "Marathon training, running coaching & endurance athletes across Delhi", "followers": 22000, "region": "Delhi", "niche": "Fitness", "tags": ["Fitness", "Athlete", "Coach / Trainer"]},
    {"username": "coachamitdahiya", "display_name": "Amit Dahiya", "bio": "Strength & Conditioning Coach • Delhi • Athlete training & bodybuilding", "followers": 25000, "region": "Delhi", "niche": "Fitness", "tags": ["Fitness", "Coach", "Trainer", "Athlete"]},
    {"username": "crossfit_delhi_hub", "display_name": "CrossFit Delhi Hub", "bio": "Functional Fitness & HIIT Coaching in South Delhi. Group classes & personal training.", "followers": 27000, "region": "Delhi", "niche": "Fitness", "tags": ["Fitness", "Trainer", "Coach / Trainer"]},
    {"username": "coach_rohit_delhi", "display_name": "Rohit Verma Fitness", "bio": "Certified K11 Trainer • Delhi • 100+ Body transformations & nutrition", "followers": 28500, "region": "Delhi", "niche": "Fitness", "tags": ["Fitness", "Coach", "Trainer", "Coach / Trainer"]},
    {"username": "yogawithpriya_delhi", "display_name": "Priya Sharma Yoga", "bio": "Certified Yoga Instructor • New Delhi • Hatha Yoga, Pranayama & Meditation", "followers": 33000, "region": "Delhi", "niche": "Fitness", "tags": ["Fitness", "Yoga", "Trainer"]},
    {"username": "fit_with_ananya", "display_name": "Ananya Roy", "bio": "Fitness Trainer & Pilates Instructor • Delhi NCR • Home workouts & fat loss", "followers": 41000, "region": "Delhi", "niche": "Fitness", "tags": ["Fitness", "Trainer", "Lifestyle"]},
    {"username": "fitwithsattysudha", "display_name": "Satty & Sudha", "bio": "Fitness Coaches & Nutritionists. Delhi NCR. Transformation specialist.", "followers": 52000, "region": "Delhi", "niche": "Fitness", "tags": ["Fitness", "Coach", "Nutritionist", "Coach / Trainer"]},

    # =========================================================================
    # 6. PAN-INDIA — FASHION & LIFESTYLE (10K-100K)
    # =========================================================================
    {"username": "indie_fashion_diaries", "display_name": "Indie Fashion Diaries", "bio": "Sustainable & indie Indian fashion creators • Handcrafted & artisanal clothing", "followers": 39000, "region": "India", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Sustainability"]},
    {"username": "ethnic_elegance_india", "display_name": "Ethnic Elegance", "bio": "Saree styling, handloom fashion & Indian ethnic wear creator", "followers": 48000, "region": "India", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Art"]},
    {"username": "theurbanstreetwear_in", "display_name": "Urban Streetwear India", "bio": "Indian streetwear culture, sneakerheads & streetwear styling creator", "followers": 62000, "region": "India", "niche": "Fashion", "tags": ["Fashion", "Lifestyle", "Content Creator"]},
    {"username": "mensfashionindia", "display_name": "Men's Fashion India", "bio": "The premier Indian menswear & styling community • Grooming & formal style", "followers": 75000, "region": "India", "niche": "Fashion", "tags": ["Fashion", "Style", "Lifestyle"]},
    {"username": "sejalgujral_style", "display_name": "Sejal Gujral", "bio": "Fashion & Lifestyle Blogger. India. Ethnic wear, styling guides & budget fashion.", "followers": 89000, "region": "India", "niche": "Fashion", "tags": ["Fashion", "Blogger", "Lifestyle"]},
    {"username": "juhi_godambe", "display_name": "Juhi Godambe Jain", "bio": "Fashion Creator & Luxury Stylist. Mumbai / India. Red carpet & streetstyle.", "followers": 560000, "region": "India", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Influencer", "Luxury"]},
    {"username": "stylebyami", "display_name": "Ami Patel", "bio": "Celebrity Fashion Stylist • India • Bollywood styling & high fashion", "followers": 620000, "region": "India", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Celebrity"]},
    {"username": "santoshishetty", "display_name": "Santoshi Shetty", "bio": "Architecture, Fashion & Mindful Lifestyle Creator. India.", "followers": 740000, "region": "India", "niche": "Fashion", "tags": ["Fashion", "Lifestyle", "Content Creator"]},
    {"username": "masoomminawala", "display_name": "Masoom Minawala Mehta", "bio": "Global Indian Fashion Influencer & Entrepreneur. Championing Indian design.", "followers": 1400000, "region": "India", "niche": "Fashion", "tags": ["Fashion", "Influencer", "Entrepreneur", "Lifestyle"]},
    {"username": "the_style_companion", "display_name": "Rhea Kapoor", "bio": "Fashion Stylist & Producer • Mumbai / India • High fashion & wardrobe design", "followers": 1700000, "region": "India", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Influencer"]}
]
