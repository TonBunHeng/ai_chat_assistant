import { tourismDataset } from '../data/tourismData';

/**
 * Perform offline tourism search directly over local tourism dataset
 * and generate answers using local Ollama model if available,
 * or provide rich local dataset responses if Ollama is not running.
 */
export const performOfflineSearch = async (query, language = 'en') => {
  const isKhmer = language === 'km' || /[\u1780-\u17FF]/.test(query || '');
  const q = query && query.toLowerCase ? query.toLowerCase().trim() : '';

  const greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'សួស្តី', 'ជម្រាបសួរ'];
  const isGreeting = greetings.includes(q) || greetings.some(g => q.startsWith(g));

  if (isGreeting) {
    return {
      success: true,
      mode: 'offline',
      intent: 'greeting',
      message: isKhmer
        ? 'សួស្តី! 🖐️ ខ្ញុំជា Angkor Verse AI ជំនួយការទេសចរណ៍ AI នៅកម្ពុជា។ តើខ្ញុំអាចជួយផ្ដល់ព័ត៌មានអំពីកន្លែងកម្សាន្ត ហាងអាហារ សណ្ឋាគារ ឬគម្រោងដើរលេងដល់អ្នកយ៉ាងដូចម្តេចដែរ?'
        : "Hello! 👋 Welcome to Cambodia! I'm Angkor Verse AI, your local AI Tourism Assistant. How can I help you explore attractions, hotels, food, or trip itineraries today?",
      suggestions: isKhmer
        ? ['តើកន្លែងណាខ្លះគួរទៅកម្សាន្តនៅសៀមរាប?', 'ម្ហូបខ្មែរណាខ្លះដែលគួរញ៉ាំ?', 'តើទៅលេងកោះរ៉ុងយ៉ាងដូចម្តេច?']
        : ['What are the best temples in Siem Reap?', 'What authentic Khmer food should I try?', 'How to visit Koh Rong island?'],
      sources: [],
    };
  }

  // Stop words that should not trigger single attraction matches
  const STOP_WORDS = new Set([
    'what', 'is', 'are', 'a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'with',
    'tell', 'me', 'about', 'how', 'where', 'which', 'who', 'why', 'cambodia', 'country', 'tourism',
    'tourist', 'visit', 'trip', 'travel', 'place', 'places', 'highlight', 'highlights', 'hi', 'hello',
    'hey', 'please', 'can', 'you', 'i', 'my', 'we', 'our', 'do', 'does', 'did',
    'កម្ពុជា', 'តើ', 'អ្វី', 'ជា', 'នៅ', 'ពី', 'អំពី', 'ទេសចរណ៍', 'កន្លែង', 'ជួយ', 'សួស្តី', 'ជំរាបសួរ'
  ]);

  const cleanQuery = q.replace(/[^\w\s\u1780-\u17FF]/g, '').trim();

  // Check if query is a broad Cambodia overview question
  const isCambodiaOverview =
    cleanQuery.includes('what is cambodia') ||
    cleanQuery.includes('tell me about cambodia') ||
    cleanQuery.includes('about cambodia') ||
    cleanQuery === 'cambodia' ||
    cleanQuery === 'cambodia country' ||
    (cleanQuery.includes('កម្ពុជា') && (cleanQuery.includes('អ្វី') || cleanQuery.includes('ប្រាប់') || cleanQuery.split(/\s+/).length <= 2));

  if (isCambodiaOverview) {
    return {
      success: true,
      mode: 'offline',
      intent: 'general_tourism',
      message: isKhmer
        ? `**ប្រទេសកម្ពុជា (ព្រះរាជាណាចក្រកម្ពុជា)** 🇰🇭\n\nកម្ពុជា គឺជាប្រទេសមួយស្ថិតនៅតំបន់អាស៊ីអាគ្នេយ៍ ដែលមានប្រវត្តិសាស្ត្រសម្បូរបែប វប្បធម៌ចំណាស់ និងសម្បត្តិបេតិកភណ្ឌពិភពលោកដ៏ល្បីល្បាញ៖\n\n- 🏛️ **រាជធានី:** ភ្នំពេញ (មជ្ឈមណ្ឌលសេដ្ឋកិច្ច និងវប្បធម៌)\n- 👑 **បេតិកភណ្ឌពិភពលោក:** ប្រាសាទអង្គរវត្ត (ខេត្តសៀមរាប), ប្រាសាទព្រះវិហារ, ប្រាសាទសម្បូរព្រៃគុក, និងកោះកេរ្តិ៍\n- 🏖️ **ឆ្នេរ និងធម្មជាតិ:** ឆ្នេរសមុទ្រ និងកោះធម្មជាតិ (ខេត្តព្រះសីហនុ និងកែប), ឧទ្យានជាតិភ្នំបូកគោ (ខេត្តកំពត)\n- 🍲 **ម្ហូបអាហារខ្មែរ:** អាម៉ុកត្រី, សម្លការីខ្មែរ, នំបញ្ចុក, ឡុកឡាក់សាច់គោ\n- 🗣️ **ភាសាផ្លូវការ:** ភាសាខ្មែរ | **រូបិយប័ណ្ណ:** រៀល (KHR) & ដុល្លារ (USD)\n\nតើអ្នកចង់ឱ្យខ្ញុំណែនាំអំពីគោលដៅទេសចរណ៍ សណ្ឋាគារ ឬរៀបចំគម្រោងដើរលេងនៅកន្លែងណាដែរ?`
        : `**Cambodia (Kingdom of Cambodia)** 🇰🇭\n\nCambodia is a captivating country in Southeast Asia renowned for its profound heritage, ancient Khmer civilization, and stunning natural landscapes:\n\n- 🏛️ **Capital:** Phnom Penh (home to the Royal Palace, National Museum, and riverside promenade)\n- 🏰 **World Heritage & Temples:** The legendary **Angkor Wat** complex, Bayon, and Ta Prohm in Siem Reap; Preah Vihear, Sambor Prei Kuk, and Koh Ker\n- 🏖️ **Islands & Coastline:** Pristine white sand beaches and tropical islands in Preah Sihanouk (Koh Rong, Koh Rong Sanloem) and Kep\n- 🌿 **Nature & Mountains:** Cardamom Mountains, Bokor National Park in Kampot, and the waterfalls of Mondulkiri\n- 🍲 **Khmer Cuisine:** Signature dishes like Fish Amok, Beef Lok Lak, Nom Banh Chok, and fresh Kampot pepper crab\n- 🗣️ **Language:** Khmer | **Currency:** Cambodian Riel (KHR) & US Dollar (USD)\n\nWould you like recommendations on itineraries, top attractions, hotels, or local transport across Cambodia?`,
      suggestions: isKhmer
        ? ['ណែនាំប្រាសាទនៅសៀមរាប', 'ណែនាំឆ្នេរនៅកំពង់សោម', 'ម្ហូបខ្មែរដែលត្រូវតែសាក']
        : ['What are top places in Siem Reap?', 'Best beaches in Koh Rong', 'Must try Cambodian food'],
      sources: [],
    };
  }

  // 1. Try local Ollama LLM if available on the client machine
  try {
    const targetLangDesc = isKhmer
      ? 'Khmer (ភាសាខ្មែរ)'
      : 'clear, natural, grammatically correct, and fluent English';

    const prompt = `SYSTEM INSTRUCTIONS:
You are Camtour-On-Mistral-Ai, an expert AI Tourism Assistant for Cambodia.
TARGET LANGUAGE: Respond strictly in ${targetLangDesc}.

RESPONSE RULES:
1. Write in clear, professional, fluent ${isKhmer ? 'Khmer' : 'English'}.
2. Ensure proper grammar, clean sentence structure, and answer the question directly.
3. Use clean markdown formatting with bullet points.
4. Do not mix Khmer characters into English responses.

User Question: '${query}'`;

    const hostname = typeof window !== 'undefined' ? window.location.hostname : 'localhost';
    const hostsToTry = [];
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      hostsToTry.push('http://localhost:11434/api/generate');
    }

    for (const url of hostsToTry) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 4000);

        const resp = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            model: 'Camtour-On-Mistral-Ai:latest',
            prompt: prompt,
            stream: false,
          }),
          signal: controller.signal,
        });
        clearTimeout(timeoutId);

        if (resp.ok) {
          const data = await resp.json();
          if (data && data.response && data.response.trim()) {
            return {
              success: true,
              mode: 'offline',
              intent: 'general',
              message: data.response.trim(),
              sources: [],
            };
          }
        }
      } catch (err) {
        // Continue to local dataset matching fallback
      }
    }
  } catch (err) {
    // Continue to local dataset matching fallback
  }

  // 2. Intelligent offline dataset search fallback on meaningful non-stopword tokens
  const queryTokens = cleanQuery.split(/\s+/).filter(t => t.length > 1 && !STOP_WORDS.has(t));
  const matchedItems = [];

  if (queryTokens.length > 0) {
    for (const item of tourismDataset) {
      let score = 0;
      const nameEn = (item.name || '').toLowerCase();
      const nameKm = (item.name_km || '').toLowerCase();
      const provEn = (item.province || '').toLowerCase();
      const provKm = (item.province_km || '').toLowerCase();
      const tags = (item.tags || []).map(t => t.toLowerCase());

      if (cleanQuery.length >= 4 && !STOP_WORDS.has(cleanQuery)) {
        if (nameEn.includes(cleanQuery) || cleanQuery.includes(nameEn)) score += 25;
        if (nameKm.includes(cleanQuery) || cleanQuery.includes(nameKm)) score += 25;
        if (provEn.includes(cleanQuery) || cleanQuery.includes(provEn)) score += 12;
      }

      for (const token of queryTokens) {
        if (nameEn === token || nameEn.split(/\s+/).includes(token)) score += 15;
        else if (nameEn.includes(token)) score += 6;

        if (nameKm === token || nameKm.includes(token)) score += 15;
        if (provEn === token || provEn.split(/\s+/).includes(token)) score += 8;
        if (tags.some(t => t === token || t.includes(token))) score += 6;
      }

      if (score >= 6) {
        matchedItems.push({ item, score });
      }
    }
  }

  matchedItems.sort((a, b) => b.score - a.score);

  if (matchedItems.length > 0) {
    const topMatches = matchedItems.slice(0, 3).map(m => m.item);
    const primary = topMatches[0];

    let messageText = '';
    if (isKhmer) {
      messageText = `**${primary.name_km || primary.name}** (${primary.category || 'ព័ត៌មានទេសចរណ៍'})\n\n`;
      messageText += `${primary.description_km || primary.description}\n\n`;
      if (primary.province) messageText += `📍 **ទីតាំង/ខេត្ត:** ${primary.province}\n`;
      if (primary.opening_hours) messageText += `⏰ **ម៉ោងបើក:** ${primary.opening_hours}\n`;
      if (primary.entrance_fee) messageText += `🎟️ **សំបុត្រ:** ${primary.entrance_fee}\n`;
      if (primary.popular_attractions) messageText += `✨ **កន្លែងល្បីៗ:** ${primary.popular_attractions.join(', ')}\n`;
      if (primary.best_time_to_visit) messageText += `🗓️ **រដូវល្អបំផុត:** ${primary.best_time_to_visit}\n`;
    } else {
      messageText = `**${primary.name}** (${primary.category || 'Tourism Highlight'})\n\n`;
      messageText += `${primary.description}\n\n`;
      if (primary.province) messageText += `📍 **Location/Province:** ${primary.province}\n`;
      if (primary.opening_hours) messageText += `⏰ **Opening Hours:** ${primary.opening_hours}\n`;
      if (primary.entrance_fee) messageText += `🎟️ **Admission:** ${primary.entrance_fee}\n`;
      if (primary.popular_attractions) messageText += `✨ **Key Highlights:** ${primary.popular_attractions.join(', ')}\n`;
      if (primary.best_time_to_visit) messageText += `🗓️ **Best Time to Visit:** ${primary.best_time_to_visit}\n`;
    }

    return {
      success: true,
      mode: 'offline',
      intent: 'tourism_search',
      message: messageText,
      sources: topMatches.map(m => ({
        name: m.name,
        title: m.name,
        category: m.category,
        location: m.province,
        description: m.description,
      })),
      suggestions: isKhmer
        ? ['តើមានកន្លែងណាទៀតដែលគួរទស្សនា?', 'តើការធ្វើដំណើរមានតម្លៃប៉ុន្មាន?', 'ណែនាំម្ហូបឆ្ងាញ់ៗនៅក្បែរនោះ']
        : ['What other places should I visit nearby?', 'How do I travel between cities?', 'Recommend local dishes to try'],
    };
  }

  // 3. Fallback response with general Cambodia travel recommendation
  return {
    success: true,
    mode: 'offline',
    intent: 'general_tourism',
    message: isKhmer
      ? `សូមស្វាគមន៍មកកាន់កម្ពុជា! 🇰🇭\n\nសម្រាប់ដំណើរកម្សាន្តនៅកម្ពុជា អ្នកអាចស្វែងយល់អំពី៖\n- 🏛️ **ប្រាសាទបុរាណ:** អង្គរវត្ត, បាយ័ន, តាព្រហ្ម (ខេត្តសៀមរាប)\n- 🏖️ **ឆ្នេរ និងកោះ:** កោះរ៉ុង, ឆ្នេរអូរឈើទាល (ខេត្តព្រះសីហនុ)\n- 🍲 **ម្ហូបអាហារ:** អាម៉ុកត្រី, នំបញ្ចុក, ឡុកឡាក់សាច់គោ\n- 🌿 **ធម្មជាតិ:** ឧទ្យានជាតិភ្នំបូកគោ (ខេត្តកំពត)\n\nតើលោកអ្នកចង់ឱ្យខ្ញុំណែនាំអំពីប្រធានបទមួយណាដែរ?`
      : `Welcome to Cambodia! 🇰🇭\n\nHere are some of the top recommendations across the Kingdom of Wonder:\n- 🏛️ **Historic Temples:** Angkor Wat, Bayon, and Ta Prohm in Siem Reap\n- 🏖️ **Beaches & Islands:** Koh Rong and Koh Rong Sanloem in Sihanoukville\n- 🍲 **Must-Try Cuisine:** Fish Amok, Nom Banh Chok, and Beef Lok Lak\n- 🌿 **Nature & Culture:** Bokor National Park in Kampot and the Royal Palace in Phnom Penh\n\nFeel free to ask for specific itineraries, tickets, or travel advice!`,
    suggestions: isKhmer
      ? ['ណែនាំប្រាសាទនៅសៀមរាប', 'ណែនាំឆ្នេរនៅកំពង់សោម', 'ម្ហូបខ្មែរដែលត្រូវតែសាក']
      : ['Tell me about Angkor Wat sunrise', 'Best beaches in Koh Rong', 'Must try Cambodian food'],
    sources: [],
  };
};

export default performOfflineSearch;
