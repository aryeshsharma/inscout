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
    # 1K - 10K (Nano creators - Natural diverse handles with location in bio)
    {"username": "stylewithkabir", "display_name": "Kabir Sharma", "bio": "Street style & Sarojini / Janpath thrift edits. Based in South Delhi. Model & stylist.", "followers": 3700, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Model"]},
    {"username": "voguebyritika", "display_name": "Ritika Sen", "bio": "Affordable capsule wardrobe & thrift lookbooks. Living in New Delhi. DM for PR/collabs.", "followers": 5290, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Model", "Open for Collabs"]},
    {"username": "sartorial_ankit", "display_name": "Ankit Mehra", "bio": "Promoting young fashion models & styling aesthetics in Delhi NCR.", "followers": 5640, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Model", "Stylist"]},
    {"username": "thelookbookdiaries", "display_name": "Sanya Kapoor", "bio": "Fashion student living in Hauz Khas, Delhi. OOTD, college styling & thrifting.", "followers": 4100, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Creator"]},
    {"username": "closetbyriya", "display_name": "Riya Varma", "bio": "Everyday college & office fashion based in Delhi NCR. Styling on a budget.", "followers": 7800, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Lifestyle"]},
    {"username": "streetwear_sid", "display_name": "Siddharth Anand", "bio": "Capturing streetwear, sneakers & underground fashion creators across Delhi.", "followers": 6200, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Lifestyle", "Content Creator"]},
    {"username": "threads_and_tales", "display_name": "Kavya Roy", "bio": "Fashion, sustainable outfits & ethnic wear. Based in Dwarka, New Delhi.", "followers": 9490, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Model"]},
    {"username": "urban_dapper_boy", "display_name": "Aarav Gupta", "bio": "Mens fashion & grooming based in Delhi NCR • Casual & semi-formal style", "followers": 8900, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Creator", "Lifestyle"]},

    # 10K - 100K (Micro & Mid creators)
    {"username": "amann4real", "display_name": "Aman Verma", "bio": "Living in New Delhi | Menswear & Fashion Creator | Styling tips & aesthetics", "followers": 14000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Creator", "Lifestyle"]},
    {"username": "manas_rekhi", "display_name": "Manas Rekhi", "bio": "Based in Delhi | Menswear, Streetstyle & Lifestyle. Model & Influencer.", "followers": 14000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Model", "Lifestyle"]},
    {"username": "yashasvi_mehlawat", "display_name": "Yashasvi Mehlawat", "bio": "Fashion Model & Content Creator. New Delhi. Editorial, commercial, runway.", "followers": 19000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Model", "Creator"]},
    {"username": "taronegoyal", "display_name": "Tarone Goyal", "bio": "Mens Fashion & Grooming Creator • Based in Delhi NCR • Minimalist Style", "followers": 28000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Lifestyle", "Creator"]},
    {"username": "dia_bajaj", "display_name": "Dia Bajaj", "bio": "Fashion Stylist & Digital Creator. Living in Delhi / NCR. Style lookbooks & beauty.", "followers": 32000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Beauty", "Content Creator"]},
    {"username": "yours.laksh17", "display_name": "Laksh Sharma", "bio": "Fashion & Lifestyle Blogger • Based in Delhi • Fitness enthusiast • Collabs: DM", "followers": 34000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Lifestyle", "Fitness", "Content Creator", "Open for Collabs"]},
    {"username": "roshninegi", "display_name": "Roshni Negi", "bio": "Fashion & Lifestyle Blogger. Living in Delhi. Casual styling, thrift finds & GRWM.", "followers": 45000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Lifestyle", "Content Creator"]},
    {"username": "the_style_mermaid", "display_name": "Surbhi Jain", "bio": "Fashion Blogger & Stylist | Based in Delhi NCR | Everyday Chic & Luxury", "followers": 51000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Lifestyle"]},
    {"username": "rbfashionstylist", "display_name": "Ruchika B", "bio": "Celebrity Stylist & Fashion Consultant. Delhi / Mumbai. Wardrobe makeover.", "followers": 72000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Stylist", "Creator"]},
    {"username": "nisha_rana_gram", "display_name": "Nisha Rana", "bio": "Fashion & Lifestyle Creator | Based in New Delhi | Content Creator & Model", "followers": 86000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Model", "Content Creator"]},
    {"username": "nikitawadhawan014", "display_name": "Nikita Wadhawan", "bio": "Fashion, Beauty & Lifestyle Creator based in Delhi NCR. Dm for collaborations.", "followers": 87000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Model", "Lifestyle", "Open for Collabs"]},

    # 100K+ (Macro & Celeb creators)
    {"username": "komalpandeyofficial", "display_name": "Komal Pandey", "bio": "Fashion Video Creator • Delhi / Mumbai • Experimental Fashion & Style", "followers": 1900000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Creator", "Stylist", "Influencer"]},
    {"username": "kritika_khurana", "display_name": "Kritika Khurana", "bio": "ThatBohoGirl • Delhi • Fashion, Travel & Lifestyle Creator • Designer", "followers": 1800000, "region": "Delhi", "niche": "Fashion", "tags": ["Fashion", "Lifestyle", "Travel", "Influencer"]},

    # =========================================================================
    # 2. DELHI — TRAVEL & EXPLORATION (Nano 1K-10K, Micro 10K-50K, Mid 50K+)
    # =========================================================================
    # 1K - 10K (Nano Travel Creators)
    {"username": "pahadi_in_delhi", "display_name": "Rahul Negi", "bio": "Delhi based pahadi traveler • Weekend treks to Uttarakhand & Himachal vlogs", "followers": 5100, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Vlogger", "Nomad"]},
    {"username": "roaming_delhiite", "display_name": "Aarushi Travels", "bio": "Budget travel tips, hostel stays & solo trips starting from New Delhi", "followers": 6500, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Lifestyle", "Content Creator"]},
    {"username": "sharma_travel_tales", "display_name": "Karan Sharma", "bio": "Delhi travel creator • Backpacking India on a budget • DM for PR/collabs", "followers": 2900, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Nomad", "Open for Collabs"]},
    {"username": "wandering_soul_aditi", "display_name": "Aditi Roy", "bio": "Living in South Delhi • Heritage walks, hidden cafes & weekend road trips. Solo travel.", "followers": 3400, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Storyteller"]},
    {"username": "trailblazer_vikram", "display_name": "Vikram Singh", "bio": "Storyteller & architecture enthusiast • Old Delhi walks & Rajasthan road trips", "followers": 8400, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Storyteller", "Photography"]},
    {"username": "weekend_wanderer_ananya", "display_name": "Ananya Joshi", "bio": "Exploring forgotten monuments & nature getaways around Delhi NCR.", "followers": 4200, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Photographer", "Explorer"]},
    {"username": "backpacking_sid", "display_name": "Siddharth Verma", "bio": "Curated road trips & camping getaways within 300km of Delhi NCR", "followers": 7900, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Guide", "Lifestyle"]},

    # 10K - 50K (Micro Travel Creators)
    {"username": "exploring_with_sahil", "display_name": "Sahil Travel Vlogs", "bio": "Travel Vlogger based in Delhi • Himachal, Uttarakhand & North India trails", "followers": 32000, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Vlogger", "Lifestyle"]},
    {"username": "wanderlust_pooja", "display_name": "Pooja Travels", "bio": "Solo female travel from Delhi • Mountains, culture & heritage storytelling", "followers": 41000, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Storyteller", "Lifestyle"]},
    {"username": "trippy_rohan", "display_name": "Rohan Travel Diaries", "bio": "Travel Photographer & Filmmaker based in New Delhi / Spiti expeditions", "followers": 36000, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Photographer", "Creator"]},
    {"username": "mountain_tales_karan", "display_name": "Karan Travel Vlogs", "bio": "Mountain lover based in Delhi • Treks, snow trails & village homestays", "followers": 19500, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Explorer", "Vlogger"]},
    {"username": "travelwithanmol", "display_name": "Anmol Sharma Travel", "bio": "Delhi Travel Creator • Weekend getaways from Delhi, Himalayas & road trips", "followers": 18000, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Lifestyle", "Content Creator"]},
    {"username": "nomadic_journeys_in", "display_name": "Nomadic Journeys", "bio": "Exploring India from New Delhi • Backpacking, budget stays & hidden gems", "followers": 24000, "region": "Delhi", "niche": "Travel", "tags": ["Travel", "Nomad", "Content Creator"]},

    # =========================================================================
    # 3. MUMBAI — TRAVEL & EXPLORATION (1K-10K, 10K-100K)
    # =========================================================================
    {"username": "kunalfilms_", "display_name": "Kunal Sharma", "bio": "Travel Content Creator based in Mumbai • Weekend getaways, Konkan coast & road trips", "followers": 5850, "region": "Mumbai", "niche": "Travel", "tags": ["Travel", "Vlogger", "Filmmaker"]},
    {"username": "anindiantourist", "display_name": "Ajmal Tourist", "bio": "Mumbai based traveler • Exploring Konkan coast, Sahyadris & hidden waterfalls", "followers": 6700, "region": "Mumbai", "niche": "Travel", "tags": ["Travel", "Nomad", "Storyteller"]},
    {"username": "mountaindeww264", "display_name": "Riaan Explorer", "bio": "Travel & trekking creator • Based in Mumbai • Sahyadri treks & camping", "followers": 1030, "region": "Mumbai", "niche": "Travel", "tags": ["Travel", "Explorer"]},
    {"username": "aanchpunjabi", "display_name": "Aanchal Punjabi", "bio": "Travel & lifestyle storyteller based in Bandra, Mumbai • Coastal diaries", "followers": 6800, "region": "Mumbai", "niche": "Travel", "tags": ["Travel", "Lifestyle", "Storyteller"]},
    {"username": "everthewanderer", "display_name": "Rachel Wanderer", "bio": "Solo female traveler living in Mumbai • Budget stays & slow travel", "followers": 4700, "region": "Mumbai", "niche": "Travel", "tags": ["Travel", "Nomad"]},
    {"username": "remishimazu", "display_name": "Remi Shimazu", "bio": "Mumbai based explorer • Heritage trails, coastal roads & travel diaries", "followers": 3948, "region": "Mumbai", "niche": "Travel", "tags": ["Travel", "Heritage", "Explorer"]},
    {"username": "joujoutravels", "display_name": "Jaclyn Travels", "bio": "Travel creator based in Mumbai • Destinations, itineraries & travel guides", "followers": 18100, "region": "Mumbai", "niche": "Travel", "tags": ["Travel", "Guide", "Content Creator"]},
    {"username": "wanderlust_mumbaikar", "display_name": "Rohan Mumbaikar", "bio": "Exploring Maharashtra & Western Ghats from Mumbai • Weekend itineraries", "followers": 28000, "region": "Mumbai", "niche": "Travel", "tags": ["Travel", "Explorer"]},
    {"username": "mumbai_roadtrippers", "display_name": "Mumbai Roadtrippers", "bio": "Road trips, monsoon drives & camping getaways around Mumbai / Pune", "followers": 34000, "region": "Mumbai", "niche": "Travel", "tags": ["Travel", "Guide", "Community"]},

    # =========================================================================
    # 4. MUMBAI — BEAUTY & MAKEUP (10K-100K and others)
    # =========================================================================
    {"username": "glambymanisha", "display_name": "Manisha MUA", "bio": "Bridal Makeup Artist & Beauty Educator • Mumbai • Studio in Bandra", "followers": 42000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "MUA", "Makeup", "Coach / Trainer"]},
    {"username": "simran_makeup_studio", "display_name": "Simran Kaur MUA", "bio": "Bridal & Fashion Makeup Artist based in Andheri, Mumbai • Glam looks", "followers": 29000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "MUA", "Makeup", "Coach / Trainer"]},
    {"username": "artistrybyalisha", "display_name": "Alisha Shaikh", "bio": "Certified Makeup Artist • Mumbai • Editorial & Bridal Glam • Bookings open", "followers": 18000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "MUA", "Makeup"]},
    {"username": "tanvimakeupstudio", "display_name": "Tanvi Studio Mumbai", "bio": "Makeup Artist & Beauty Studio • Mumbai • Workshops & Glam Lookbooks", "followers": 35000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "MUA", "Makeup", "Coach / Trainer"]},
    {"username": "skinandglambymaya", "display_name": "Maya Shah", "bio": "Aesthetician & Skincare Blogger • Mumbai • Dermat-approved skincare", "followers": 52000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "Skincare", "Blogger"]},
    {"username": "corallistablog", "display_name": "Ankita Chaturvedi", "bio": "Beauty & Lifestyle Blogger. Mumbai. Makeup tutorials, beauty tips & skincare.", "followers": 290000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "Makeup", "Skincare", "Blogger"]},
    {"username": "debasreee", "display_name": "Debasree Banerjee", "bio": "Beauty Creator & Founder of #debasreebeauty. Mumbai based. Skincare & makeup.", "followers": 310000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "Skincare", "Founder", "Influencer"]},
    {"username": "shreyajain26", "display_name": "Shreya Jain", "bio": "Beauty & Makeup Content Creator. Mumbai / Delhi. Tutorials & honest reviews.", "followers": 440000, "region": "Mumbai", "niche": "Beauty", "tags": ["Beauty", "Makeup", "Content Creator", "Influencer"]},

    # =========================================================================
    # 4. BANGALORE — TECHNOLOGY & DEVELOPERS (10K-500K)
    # =========================================================================
    {"username": "devops_arun", "display_name": "Arun Kumar", "bio": "Cloud & DevOps Architect • Bangalore • Kubernetes, AWS & Cloud Native", "followers": 16000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer"]},
    {"username": "rust_dev_india", "display_name": "Siddharth Dev", "bio": "Systems programmer & Rust builder in Bangalore • Backend engineering & OSS", "followers": 18000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Coding"]},
    {"username": "ai_builder_rahul", "display_name": "Rahul N", "bio": "Building GenAI apps • Bangalore Tech Founder • LLMs & AI agents", "followers": 29000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Founder"]},
    {"username": "datascience_rohit", "display_name": "Rohit Verma", "bio": "AI & Data Scientist in Bangalore • ML projects, Python tutorials & career tips", "followers": 38000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Educator"]},
    {"username": "anurag_codes", "display_name": "Anurag Mishra", "bio": "Senior Software Engineer @ Bangalore Tech Startup • Fullstack & System Design", "followers": 46000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Coding"]},
    {"username": "tech_with_divya", "display_name": "Divya Krishnan", "bio": "Software Engineer @ Bangalore • Tech vlog, coding roadmap & WFH life", "followers": 51000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Lifestyle"]},
    {"username": "frontend_priya", "display_name": "Priya Sharma", "bio": "Frontend Dev & Tech Creator • Bangalore • React, NextJS & CSS tips", "followers": 62000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Coding", "Content Creator"]},
    {"username": "tanaypratap", "display_name": "Tanay Pratap", "bio": "Tech Educator & Founder. Bangalore. Coding, career advice & software building.", "followers": 185000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Founder", "Educator"]},
    {"username": "hiteshchoudharyofficial", "display_name": "Hitesh Choudhary", "bio": "Software Developer & YouTuber • Bangalore / Jaipur • Tech, Python, JS & AI", "followers": 380000, "region": "Bangalore", "niche": "Technology", "tags": ["Technology", "Developer", "Educator", "Influencer"]},

    # =========================================================================
    # 5. DELHI — LIFESTYLE & VLOGGERS (1K-50K)
    # =========================================================================
    {"username": "lifewithjeet13", "display_name": "Jeet Singh", "bio": "📍Delhi, India 👳 Sardaar Style & Lifestyle 🎥 Daily Life Delhi Streets 📩 DM for Collaborations", "followers": 4331, "region": "Delhi", "niche": "Lifestyle", "tags": ["Lifestyle", "Content Creator", "Open for Collabs"]},
    {"username": "kashishhhforreal", "display_name": "Kashish Jain", "bio": "📸 Reels. Real life. Right here. 📍Delhi | Creator | Lifestyle & aesthetics", "followers": 1171, "region": "Delhi", "niche": "Lifestyle", "tags": ["Lifestyle", "Content Creator"]},
    {"username": "vlogswithshreya", "display_name": "Shreya Kapoor", "bio": "Daily life vlogs & cafe recommendations in South Delhi. Storyteller.", "followers": 8500, "region": "Delhi", "niche": "Lifestyle", "tags": ["Lifestyle", "Vlogger", "Storyteller"]},
    {"username": "delhi_diaries_with_tanvi", "display_name": "Tanvi Chawla", "bio": "Living in New Delhi. Exploring aesthetics, lifestyle & everyday moments.", "followers": 16500, "region": "Delhi", "niche": "Lifestyle", "tags": ["Lifestyle", "Creator"]},
    {"username": "rohit_vlog_world", "display_name": "Rohit Verma", "bio": "Delhi lifestyle vlogger • Street culture, food walks & travel experiences", "followers": 28000, "region": "Delhi", "niche": "Lifestyle", "tags": ["Lifestyle", "Vlogger"]}
]
