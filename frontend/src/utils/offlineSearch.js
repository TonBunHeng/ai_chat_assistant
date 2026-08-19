
/**
 * Perform offline tourism search directly over local tourism.json dataset.
 */
/**
 * Perform offline tourism search directly over local tourism.json dataset
 * and generate answers using local Ollama model if available.
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
      sources: [],
    };
  }

  // Query Camtour-On-Mistral-Ai directly with zero external database RAG context
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

    const hostname = window.location.hostname || 'localhost';
    const hostsToTry = [`http://${hostname}:11434/api/generate`];
    if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
      hostsToTry.push('http://localhost:11434/api/generate');
    }

    for (const url of hostsToTry) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 15000);

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
        console.warn(`Direct client-side Camtour-On-Mistral-Ai call to ${url} unreached:`, err);
      }
    }
  } catch (err) {
    console.warn('Direct client-side Camtour-On-Mistral-Ai call error:', err);
  }

  return {
    success: true,
    mode: 'offline',
    intent: 'general',
    message: isKhmer
      ? 'សូមអភ័យទោស៖ មិនអាចភ្ជាប់ទៅកាន់ម៉ូឌែល Camtour-On-Mistral-Ai បានទេ។ សូមពិនិត្យមើលថាសេវាកម្ម Ollama របស់លោកអ្នកកំពុងដំណើរកា។'
      : 'Sorry: Unable to connect to local Camtour-On-Mistral-Ai model. Please ensure Ollama service is active.',
    sources: [],
  };
};

export default performOfflineSearch;
