export const tourismDataset = [
  // Destinations
  {
    id: "dest_sr",
    name: "Siem Reap",
    name_km: "សៀមរាប",
    province: "Siem Reap",
    category: "Destination",
    description: "Gateway to the ancient Angkor region, world famous for Angkor Wat, Pub Street, and rich Khmer heritage.",
    description_km: "ច្រកចូលទៅកាន់តំបន់អង្គរដ៏អស្ចារ្យ ព័ទ្ធជុំវិញដោយប្រាសាទបុរាណ ផ្លូវដើររាត្រី (Pub Street) និងវប្បធម៌ខ្មែរ។",
    popular_attractions: ["Angkor Wat", "Bayon Temple", "Ta Prohm", "Pub Street", "Tonle Sap Lake"],
    best_time_to_visit: "November to February",
    tags: ["Siem Reap", "Angkor", "Heritage", "Temples", "Pub Street"]
  },
  {
    id: "dest_pp",
    name: "Phnom Penh",
    name_km: "ភ្នំពេញ",
    province: "Phnom Penh",
    category: "Destination",
    description: "Capital city of Cambodia situated at the confluence of Tonle Sap, Mekong, and Bassac Rivers.",
    description_km: "រាជធានីនៃប្រទេសកម្ពុជា ស្ថិតនៅចតុមុខនៃទន្លេសាប ទន្លេមេគង្គ និងទន្លេបាសាក់។",
    popular_attractions: ["Royal Palace", "National Museum", "Wat Phnom", "Central Market", "Riverside"],
    best_time_to_visit: "November to March",
    tags: ["Capital", "Phnom Penh", "Museum", "Palace", "Riverside"]
  },
  {
    id: "dest_kr",
    name: "Koh Rong",
    name_km: "កោះរ៉ុង",
    province: "Preah Sihanouk",
    category: "Beach Destination",
    description: "Famous island known for white sand beaches, turquoise waters, bioluminescent plankton, and relaxing resorts.",
    description_km: "កោះដ៏ល្បីល្បាញដែលមានឆ្នេរខ្សាច់សស្អាត ទឹកសមុទ្រថ្លាយ៉ង់ និងពន្លឺផ្លេកៗនៃប្លង់តុងនាពេលរាត្រី។",
    popular_attractions: ["Long Set Beach", "Sok San Beach", "Bioluminescent Plankton", "Koh Rong Sanloem"],
    best_time_to_visit: "December to May",
    tags: ["Beach", "Island", "Sihanoukville", "Resort", "Snorkeling"]
  },
  {
    id: "dest_kp",
    name: "Kampot",
    name_km: "កំពត",
    province: "Kampot",
    category: "Riverside Town",
    description: "Charming riverside city famous for Kampot pepper farms, French colonial architecture, and Bokor Mountain.",
    description_km: "ក្រុងមាត់ព្រែកដ៏ស្រស់ស្អាត ល្បីល្បាញដោយសារម្រេចកំពត ស្ថាបត្យកម្មបារាំង និងភ្នំបូកគោ។",
    popular_attractions: ["Bokor National Park", "Kampot River", "Pepper Farms", "Salt Fields", "Rabbit Island"],
    best_time_to_visit: "November to April",
    tags: ["Kampot", "Bokor", "Pepper", "Nature", "River"]
  },

  // Temples
  {
    id: "tpl_angkorwat",
    name: "Angkor Wat",
    name_km: "ប្រាសាទអង្គរវត្ត",
    province: "Siem Reap",
    category: "Temple",
    description: "Largest religious monument in the world, built by King Suryavarman II in the 12th century. Famous for sunrise views and intricate bas-reliefs.",
    description_km: "វិមានសាសនាធំជាងគេបំផុតនៅលើពិភពលោក កសាងឡើងដោយព្រះបាទសូរ្យវរ្ម័នទី២ នៅសតវត្សរ៍ទី១២។ ល្បីល្បាញខ្លាំងពេលថ្ងៃរះ។",
    opening_hours: "05:00 AM - 05:30 PM",
    entrance_fee: "Included in Angkor Pass ($37 1-day, $62 3-day, $72 7-day)",
    tags: ["Heritage", "UNESCO", "Temple", "Siem Reap", "Architecture", "Angkor"]
  },
  {
    id: "tpl_bayon",
    name: "Bayon Temple",
    name_km: "ប្រាសាទបាយ័ន",
    province: "Siem Reap",
    category: "Temple",
    description: "Iconic temple at the center of Angkor Thom known for its 216 giant smiling face towers of Avalokiteshvara.",
    description_km: "ប្រាសាទដ៏ល្បីល្បាញនៅចំកណ្តាលអង្គរធំ មានកំពូលមុខញញឹមចំនួន ២១៦ ដែលតំណាងឲ្យព្រះពោធិសត្វលោកេសិវរ។",
    opening_hours: "07:30 AM - 05:30 PM",
    entrance_fee: "Included in Angkor Pass",
    tags: ["Heritage", "Angkor Thom", "Temple", "Siem Reap", "Faces"]
  },
  {
    id: "tpl_taprohm",
    name: "Ta Prohm",
    name_km: "ប្រាសាទតាព្រហ្ម",
    province: "Siem Reap",
    category: "Temple",
    description: "Famous 'Tomb Raider' temple left largely as it was found, entwined with giant silk-cotton tree roots.",
    description_km: "ប្រាសាទដែលល្បីល្បាញតាមរយៈរឿង Tomb Raider ដែលមានឫសឈើធំៗព័ទ្ធជុំវិញជញ្ជាំងប្រាសាទ។",
    opening_hours: "07:30 AM - 05:30 PM",
    entrance_fee: "Included in Angkor Pass",
    tags: ["Heritage", "Nature", "Temple", "Siem Reap", "Tomb Raider"]
  },

  // Food
  {
    id: "food_amok",
    name: "Fish Amok",
    name_km: "អាម៉ុកត្រី",
    category: "Food",
    province: "Nationwide",
    description: "Cambodia's signature national dish made from steamed fish cooked in coconut milk, kroeung paste, and noni leaves served in banana leaf bowls.",
    description_km: "ម្ហូបតំណាងជាតិកម្ពុជា ធ្វើអំពីត្រីចំហុយជាមួយគ្រឿងខ្ទិះដូង ស្លឹកញ និងគ្រឿងកែច្នៃខ្មែរ រៀបចំក្នុងកកោសស្លឹកចេក។",
    tags: ["Traditional", "Must Try", "Khmer Food", "Curry", "Food"]
  },
  {
    id: "food_nombanhchok",
    name: "Nom Banh Chok",
    name_km: "នំបញ្ចុក",
    category: "Food",
    province: "Nationwide",
    description: "Traditional Khmer rice noodles served with fragrant green fish curry sauce and freshly chopped herbs and vegetables.",
    description_km: "នំបញ្ចុកស្រស់ទទួលទានជាមួយសម្លប្រហើរត្រី និងបន្លែស្រស់ជាច្រើនមុខ។",
    tags: ["Noodles", "Breakfast", "Street Food", "Traditional", "Food"]
  },
  {
    id: "food_loklak",
    name: "Beef Lok Lak",
    name_km: "ឡុកឡាក់សាច់គោ",
    category: "Food",
    province: "Nationwide",
    description: "Stir-fried marinated beef cubes served over lettuce, tomatoes, cucumbers, and a lime pepper dipping sauce.",
    description_km: "សាច់គោឆាគ្រឿងបំពង ញ៉ាំជាមួយបន្លែស្រស់ និងទឹកត្រចៀកកាំក្រូចឆ្មារម្រេច។",
    tags: ["Beef", "Dinner", "Popular", "Food"]
  },

  // Beaches
  {
    id: "beach_kohrong",
    name: "Koh Rong Island & Sanloem",
    name_km: "ឆ្នេរកោះរ៉ុង និងកោះរ៉ុងសន្លឹម",
    province: "Preah Sihanouk",
    category: "Beach",
    description: "Stunning white sand beaches, crystal clear waters, coral reefs, and evening bioluminescent plankton tours.",
    description_km: "ឆ្នេរខ្សាច់សស្អាត ទឹកសមុទ្រថ្លាយ៉ង់ មានផ្ទះលំហែកាយ និងកន្លែងមុជទឹកមើលផ្កាថ្ម។",
    tags: ["Beach", "Island", "Sihanoukville", "Snorkeling", "Relax"]
  },

  // Travel Tips
  {
    id: "tip_currency",
    name: "Currency & Payments",
    name_km: "រូបិយវត្ថុ និងការទូទាត់",
    category: "Travel Tip",
    province: "Nationwide",
    description: "US Dollars (USD) and Cambodian Riel (KHR) are both accepted nationwide ($1 USD ≈ 4,100 KHR). Bakong KHQR digital payment is widely accepted in restaurants and shops.",
    description_km: "ប្រាក់ដុល្លារអាមេរិក (USD) និងប្រាក់រៀល (KHR) ត្រូវបានប្រើប្រាស់ទូទាំងប្រទេស។ $1 USD = ៤,១០០ រៀល។ ការទូទាត់តាម KHQR មានប្រជាប្រិយភាពខ្លាំង។",
    tags: ["Money", "USD", "Riel", "Bakong", "KHQR", "Currency"]
  },
  {
    id: "tip_weather",
    name: "Weather & Dress Code",
    name_km: "អាកាសធាតុ និងការស្លៀកពាក់",
    category: "Travel Tip",
    province: "Nationwide",
    description: "Tropical climate. Best time to visit is November to February (cool & dry). Dress respectfully (cover shoulders and knees) when visiting ancient temples and royal palaces.",
    description_km: "អាកាសធាតុក្តៅសើម។ រដូវល្អបំផុតគឺខែវិច្ឆិកា ដល់កុម្ភៈ។ សូមស្លៀកពាក់រៀបរយ (គ្របស្មា និងជង្គង់) ពេលចូលទស្សនាប្រាសាទ។",
    tags: ["Weather", "Clothing", "Temples", "Dress Code", "Season"]
  }
];

export default tourismDataset;
