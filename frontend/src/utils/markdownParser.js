/**
 * Lightweight, robust, self-contained Markdown and Code syntax parser.
 * Zero external dependencies. Safe against XSS by escaping HTML entities first.
 */

// Escape HTML characters to prevent XSS
export function escapeHtml(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/**
 * Syntax highlighter for common programming languages
 */
export function highlightCode(code, lang = '') {
  const safe = escapeHtml(code);
  const cleanLang = (lang || '').toLowerCase().trim();

  // Keyword sets based on language
  const keywords = [
    'def', 'class', 'import', 'from', 'return', 'if', 'elif', 'else', 'for', 'while',
    'try', 'except', 'finally', 'with', 'as', 'lambda', 'async', 'await', 'yield',
    'function', 'const', 'let', 'var', 'export', 'default', 'new', 'this', 'typeof',
    'instanceof', 'switch', 'case', 'break', 'continue', 'throw', 'catch', 'package',
    'public', 'private', 'protected', 'static', 'void', 'int', 'float', 'string',
    'boolean', 'interface', 'implements', 'extends', 'SELECT', 'FROM', 'WHERE',
    'JOIN', 'INNER', 'LEFT', 'RIGHT', 'GROUP BY', 'ORDER BY', 'INSERT', 'UPDATE', 'DELETE'
  ];

  const keywordRegex = new RegExp(`\\b(${keywords.join('|')})\\b`, 'g');

  // Syntax color rules
  let highlighted = safe
    // Strings in double or single quotes
    .replace(/(&quot;.*?&quot;|&#039;.*?&#039;|`.*?`)/g, '<span class="text-emerald-500 dark:text-emerald-400">$1</span>')
    // Comments (#, //, --)
    .replace(/(#.*|\/\/.*|--.*)$/gm, '<span class="text-zinc-400 dark:text-zinc-500 italic">$1</span>')
    // Numbers
    .replace(/\b(\d+(\.\d+)?)\b/g, '<span class="text-amber-500 dark:text-amber-400">$1</span>')
    // Keywords
    .replace(keywordRegex, '<span class="text-purple-600 dark:text-purple-400 font-semibold">$1</span>');

  return highlighted;
}

/**
 * Parses full markdown string into structured HTML.
 */
export function parseMarkdown(rawMarkdown) {
  if (!rawMarkdown) return '';

  const blocks = [];
  const lines = rawMarkdown.split('\n');
  let inCodeBlock = false;
  let codeLang = '';
  let codeBuffer = [];
  let inTable = false;
  let tableRows = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Fenced Code Blocks (```lang)
    const codeFenceMatch = line.match(/^```(\w*)/);
    if (codeFenceMatch) {
      if (inCodeBlock) {
        // End code block
        const codeText = codeBuffer.join('\n');
        blocks.push({
          type: 'code',
          lang: codeLang || 'text',
          rawCode: codeText,
          html: highlightCode(codeText, codeLang),
        });
        codeBuffer = [];
        inCodeBlock = false;
        codeLang = '';
      } else {
        // Flush any table
        if (inTable) {
          blocks.push({ type: 'table', rows: tableRows });
          tableRows = [];
          inTable = false;
        }
        // Start code block
        inCodeBlock = true;
        codeLang = codeFenceMatch[1] || '';
      }
      continue;
    }

    if (inCodeBlock) {
      codeBuffer.push(line);
      continue;
    }

    // Markdown Table (| col1 | col2 |)
    const tableMatch = line.trim().startsWith('|') && line.trim().endsWith('|');
    if (tableMatch) {
      // Check if separator line (|---|---|)
      const isSep = /^\|[\s-:]+(\|[\s-:]+)+\|$/.test(line.trim());
      if (isSep) {
        // Table header separator, mark previous row as header
        if (tableRows.length > 0) {
          tableRows[tableRows.length - 1].isHeader = true;
        }
      } else {
        const cells = line
          .trim()
          .slice(1, -1)
          .split('|')
          .map((c) => parseInline(c.trim()));
        tableRows.push({ cells, isHeader: false });
      }
      inTable = true;
      continue;
    } else if (inTable) {
      blocks.push({ type: 'table', rows: tableRows });
      tableRows = [];
      inTable = false;
    }

    // Headers (# H1, ## H2, ### H3, #### H4)
    const hMatch = line.match(/^(#{1,4})\s+(.+)$/);
    if (hMatch) {
      const level = hMatch[1].length;
      blocks.push({
        type: `h${level}`,
        html: parseInline(hMatch[2].trim()),
      });
      continue;
    }

    // Blockquote (> quote)
    if (line.startsWith('> ')) {
      blocks.push({
        type: 'blockquote',
        html: parseInline(line.slice(2).trim()),
      });
      continue;
    }

    // Horizontal Rule (--- or ***)
    if (/^(\*{3,}|-{3,})$/.test(line.trim())) {
      blocks.push({ type: 'hr' });
      continue;
    }

    // Unordered List (- or *)
    const ulMatch = line.match(/^(\s*)[-*]\s+(.+)$/);
    if (ulMatch) {
      blocks.push({
        type: 'ul_item',
        indent: ulMatch[1].length,
        html: parseInline(ulMatch[2].trim()),
      });
      continue;
    }

    // Ordered List (1. 2. 3.)
    const olMatch = line.match(/^(\s*)(\d+)\.\s+(.+)$/);
    if (olMatch) {
      blocks.push({
        type: 'ol_item',
        number: olMatch[2],
        html: parseInline(olMatch[3].trim()),
      });
      continue;
    }

    // Empty lines
    if (!line.trim()) {
      blocks.push({ type: 'spacer' });
      continue;
    }

    // Standard paragraph line
    blocks.push({
      type: 'p',
      html: parseInline(line.trim()),
    });
  }

  // Flush trailing code block if unterminated (e.g. streaming in progress)
  if (inCodeBlock && codeBuffer.length > 0) {
    const codeText = codeBuffer.join('\n');
    blocks.push({
      type: 'code',
      lang: codeLang || 'text',
      rawCode: codeText,
      html: highlightCode(codeText, codeLang),
      isStreaming: true,
    });
  }

  // Flush trailing table
  if (inTable && tableRows.length > 0) {
    blocks.push({ type: 'table', rows: tableRows });
  }

  return blocks;
}

/**
 * Parses inline formatting: bold, italic, inline code, links
 */
export function parseInline(text) {
  if (!text) return '';

  let s = escapeHtml(text);

  // Inline code: `code`
  s = s.replace(/`([^`]+)`/g, '<code class="px-1.5 py-0.5 rounded-md bg-zinc-100 dark:bg-zinc-800 text-purple-600 dark:text-purple-400 font-mono text-[13px] border border-zinc-200 dark:border-zinc-700/60">$1</code>');

  // Bold: **text** or __text__
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong class="font-semibold text-zinc-900 dark:text-zinc-100">$1</strong>');
  s = s.replace(/__([^_]+)__/g, '<strong class="font-semibold text-zinc-900 dark:text-zinc-100">$1</strong>');

  // Italic: *text* or _text_
  s = s.replace(/\*([^*]+)\*/g, '<em class="italic text-zinc-800 dark:text-zinc-200">$1</em>');
  s = s.replace(/_([^_]+)_/g, '<em class="italic text-zinc-800 dark:text-zinc-200">$1</em>');

  // Strikethrough: ~~text~~
  s = s.replace(/~~([^~]+)~~/g, '<del class="line-through text-zinc-400">$1</del>');

  // Links: [text](url)
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="text-blue-600 dark:text-blue-400 underline underline-offset-2 hover:text-blue-700 dark:hover:text-blue-300 font-medium">$1</a>');

  return s;
}
