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

  // 2. Intelligent offline dataset search fallback
  const queryTokens = q.split(/\s+/).filter(Boolean);
  const matchedItems = [];

  for (const item of tourismDataset) {
    let score = 0;
    const itemText = [
      item.name,
      item.name_km,
      item.province,
      item.category,
      item.description,
      item.description_km,
      ...(item.tags || []),
      ...(item.popular_attractions || [])
    ].join(' ').toLowerCase();

    for (const token of queryTokens) {
      if (token.length > 2 && itemText.includes(token)) {
        score += 1;
      }
    }

    if (score > 0) {
      matchedItems.push({ item, score });
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
