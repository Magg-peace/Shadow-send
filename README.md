const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
  LevelFormat, ExternalHyperlink
} = require('docx');
const fs = require('fs');

const PURPLE = '6342FF';
const PURPLE_LIGHT = 'EDE9FF';
const TEAL = '0E7490';
const TEAL_LIGHT = 'E0F7FA';
const DARK = '1A1A2E';
const MID = '4B5563';
const LIGHT_BG = 'F8F7FF';
const BORDER_COLOR = 'DDD6FE';
const GREEN = '166534';
const GREEN_BG = 'DCFCE7';
const AMBER = '92400E';
const AMBER_BG = 'FEF3C7';

function hRule() {
  return new Paragraph({
    children: [],
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: PURPLE, space: 1 } },
    spacing: { before: 200, after: 200 }
  });
}

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun({ text, font: 'Arial', size: 36, bold: true, color: PURPLE })],
    spacing: { before: 400, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: BORDER_COLOR, space: 4 } }
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    children: [new TextRun({ text, font: 'Arial', size: 26, bold: true, color: DARK })],
    spacing: { before: 320, after: 100 }
  });
}

function heading3(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: 'Arial', size: 22, bold: true, color: TEAL })],
    spacing: { before: 200, after: 80 }
  });
}

function para(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, font: 'Arial', size: opts.size || 22, color: opts.color || MID, bold: opts.bold || false })],
    spacing: { before: opts.spaceBefore || 60, after: opts.spaceAfter || 60 },
    alignment: opts.align || AlignmentType.LEFT
  });
}

function bullet(text, emoji = '•') {
  const parts = text.split(/(\*\*.*?\*\*)/g);
  const runs = parts.map(p => {
    if (p.startsWith('**') && p.endsWith('**')) {
      return new TextRun({ text: p.slice(2, -2), font: 'Arial', size: 22, color: DARK, bold: true });
    }
    return new TextRun({ text: p, font: 'Arial', size: 22, color: MID });
  });
  return new Paragraph({
    numbering: { reference: 'bullets', level: 0 },
    children: runs,
    spacing: { before: 40, after: 40 }
  });
}

function codeBlock(lines) {
  const border = { style: BorderStyle.SINGLE, size: 1, color: '374151' };
  const borders = { top: border, bottom: border, left: border, right: border };
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [new TableRow({
      children: [new TableCell({
        borders,
        shading: { fill: '111827', type: ShadingType.CLEAR },
        margins: { top: 160, bottom: 160, left: 240, right: 240 },
        width: { size: 9360, type: WidthType.DXA },
        children: lines.map(l => new Paragraph({
          children: [new TextRun({ text: l, font: 'Courier New', size: 18, color: '86EFAC' })],
          spacing: { before: 20, after: 20 }
        }))
      })]
    })]
  });
}

function badgeTable(badges) {
  // Each badge: { label, value, bg, textColor }
  const cellW = Math.floor(9360 / badges.length);
  const colWidths = badges.map((_, i) => i === badges.length - 1 ? 9360 - cellW * (badges.length - 1) : cellW);
  const noBorder = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
  const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [new TableRow({
      children: badges.map((b, i) => new TableCell({
        borders: noBorders,
        shading: { fill: b.bg, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        width: { size: colWidths[i], type: WidthType.DXA },
        children: [
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: b.label, font: 'Arial', size: 17, color: b.textColor, bold: true })]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: b.value, font: 'Arial', size: 20, color: b.textColor, bold: false })]
          })
        ]
      }))
    })]
  });
}

function infoBox(lines, bg, borderColor, textColor) {
  const border = { style: BorderStyle.SINGLE, size: 1, color: borderColor };
  const borders = { top: border, bottom: border, left: { style: BorderStyle.SINGLE, size: 12, color: borderColor }, right: border };
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [new TableRow({
      children: [new TableCell({
        borders,
        shading: { fill: bg, type: ShadingType.CLEAR },
        margins: { top: 120, bottom: 120, left: 200, right: 200 },
        width: { size: 9360, type: WidthType.DXA },
        children: lines.map(l => new Paragraph({
          children: [new TextRun({ text: l, font: 'Arial', size: 21, color: textColor })],
          spacing: { before: 40, after: 40 }
        }))
      })]
    })]
  });
}

function twoColTable(rows, header = null) {
  const border = { style: BorderStyle.SINGLE, size: 1, color: BORDER_COLOR };
  const borders = { top: border, bottom: border, left: border, right: border };
  const tableRows = [];

  if (header) {
    tableRows.push(new TableRow({
      children: header.map((h, i) => new TableCell({
        borders,
        shading: { fill: PURPLE, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 140, right: 140 },
        width: { size: i === 0 ? 3600 : 5760, type: WidthType.DXA },
        children: [new Paragraph({ children: [new TextRun({ text: h, font: 'Arial', size: 20, color: 'FFFFFF', bold: true })] })]
      }))
    }));
  }

  rows.forEach((row, ri) => {
    tableRows.push(new TableRow({
      children: row.map((cell, ci) => new TableCell({
        borders,
        shading: { fill: ri % 2 === 0 ? 'FFFFFF' : LIGHT_BG, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 140, right: 140 },
        width: { size: ci === 0 ? 3600 : 5760, type: WidthType.DXA },
        children: [new Paragraph({ children: [new TextRun({ text: cell, font: 'Arial', size: 20, color: ci === 0 ? DARK : MID, bold: ci === 0 })] })]
      }))
    }));
  });

  return new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: [3600, 5760], rows: tableRows });
}

function spacer(before = 100) {
  return new Paragraph({ children: [], spacing: { before, after: 0 } });
}

const doc = new Document({
  numbering: {
    config: [
      {
        reference: 'bullets',
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: '\u2022',
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 560, hanging: 280 } } }
        }]
      },
      {
        reference: 'steps',
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: '%1.',
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 600, hanging: 360 } } }
        }]
      }
    ]
  },
  styles: {
    default: { document: { run: { font: 'Arial', size: 22 } } },
    paragraphStyles: [
      {
        id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 36, bold: true, font: 'Arial' },
        paragraph: { spacing: { before: 400, after: 120 }, outlineLevel: 0 }
      },
      {
        id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 26, bold: true, font: 'Arial' },
        paragraph: { spacing: { before: 320, after: 100 }, outlineLevel: 1 }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [

      // ── TITLE BLOCK ──────────────────────────────────
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: '🔐', font: 'Arial', size: 64 })],
        spacing: { before: 0, after: 80 }
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: 'ShadowSend PRO', font: 'Arial', size: 56, bold: true, color: PURPLE })],
        spacing: { before: 0, after: 60 }
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: 'Secure Image-Based Messaging using Cryptography & Steganography', font: 'Arial', size: 24, color: MID })],
        spacing: { before: 0, after: 200 }
      }),

      // Badge row
      badgeTable([
        { label: 'Built with', value: 'Python · Streamlit', bg: PURPLE_LIGHT, textColor: '4C1D95' },
        { label: 'Encryption', value: 'AES-128 / Fernet', bg: TEAL_LIGHT, textColor: '134E4A' },
        { label: 'Technique', value: 'LSB Steganography', bg: GREEN_BG, textColor: GREEN },
        { label: 'Interface', value: 'Web Browser', bg: AMBER_BG, textColor: AMBER }
      ]),

      spacer(240),
      hRule(),
      spacer(100),

      // ── OVERVIEW ─────────────────────────────────────
      heading1('🚀 Overview'),
      spacer(60),
      infoBox([
        'ShadowSend PRO is a web-based secure communication application that allows users to hide',
        'secret messages inside images. It combines AES encryption and LSB steganography to ensure',
        'that messages remain both encrypted and invisible to the naked eye.',
        '',
        'Built with Streamlit, it provides a clean, interactive interface accessible via any web browser.'
      ], LIGHT_BG, PURPLE, DARK),

      spacer(160),

      // ── FEATURES ─────────────────────────────────────
      heading1('✨ Features'),
      spacer(60),
      bullet('**🔐 AES Encryption** — Message encrypted using Fernet (AES-128-CBC) before hiding'),
      bullet('**🔑 SHA-256 Key Derivation** — Password converted to secure key via SHA-256 hash'),
      bullet('**🖼️ LSB Steganography** — Encrypted data embedded in pixel least-significant bits'),
      bullet('**📤 Encode Mode** — Upload image, type message, set password, download secret image'),
      bullet('**📥 Decode Mode** — Upload secret image, enter password, reveal hidden message'),
      bullet('**🎨 Modern Streamlit UI** — Clean, browser-based interface with no setup needed'),
      bullet('**🔎 Password Strength Indicator** — Live feedback on password quality'),
      bullet('**🖼️ Image Preview** — Side-by-side comparison of original vs. encoded image'),
      bullet('**📥 Download Encoded Image** — One-click download of the stego image'),

      spacer(160),

      // ── HOW IT WORKS ─────────────────────────────────
      heading1('🧠 How It Works'),
      spacer(60),

      new Paragraph({
        numbering: { reference: 'steps', level: 0 },
        children: [new TextRun({ text: 'User enters a secret message and a password into the web interface', font: 'Arial', size: 22, color: MID })],
        spacing: { before: 60, after: 60 }
      }),
      new Paragraph({
        numbering: { reference: 'steps', level: 0 },
        children: [new TextRun({ text: 'Password is converted into a 32-byte AES-compatible key using SHA-256', font: 'Arial', size: 22, color: MID })],
        spacing: { before: 60, after: 60 }
      }),
      new Paragraph({
        numbering: { reference: 'steps', level: 0 },
        children: [new TextRun({ text: 'Message is encrypted using Fernet (AES-128 symmetric encryption)', font: 'Arial', size: 22, color: MID })],
        spacing: { before: 60, after: 60 }
      }),
      new Paragraph({
        numbering: { reference: 'steps', level: 0 },
        children: [new TextRun({ text: 'Encrypted bytes are embedded into image pixels by modifying each pixel\'s least-significant bit (LSB) — a change invisible to the human eye', font: 'Arial', size: 22, color: MID })],
        spacing: { before: 60, after: 60 }
      }),
      new Paragraph({
        numbering: { reference: 'steps', level: 0 },
        children: [new TextRun({ text: 'Receiver uploads the stego image and enters the correct password', font: 'Arial', size: 22, color: MID })],
        spacing: { before: 60, after: 60 }
      }),
      new Paragraph({
        numbering: { reference: 'steps', level: 0 },
        children: [new TextRun({ text: 'Application extracts the LSB data, reconstructs the encrypted bytes, and decrypts the original message', font: 'Arial', size: 22, color: MID })],
        spacing: { before: 60, after: 60 }
      }),

      spacer(120),
      infoBox([
        '🔒  Security Note: Even if an attacker intercepts the image and discovers it contains',
        '     hidden data, they still cannot read the message without the correct password.',
        '     This is the dual-layer protection: Steganography hides the existence of the',
        '     message; Encryption hides the content of the message.'
      ], AMBER_BG, 'D97706', '78350F'),

      spacer(160),

      // ── TECH STACK ───────────────────────────────────
      heading1('🛠️ Tech Stack'),
      spacer(60),
      twoColTable([
        ['Python 3.x', 'Core programming language'],
        ['Streamlit', 'Web application framework — browser-based UI'],
        ['cryptography', 'Fernet encryption (AES-128) + SHA-256 key derivation'],
        ['NumPy', 'Pixel array manipulation for LSB operations'],
        ['Pillow (PIL)', 'Image loading, conversion, and saving (PNG)']
      ], ['Component', 'Purpose']),

      spacer(160),

      // ── PROJECT STRUCTURE ─────────────────────────────
      heading1('📂 Project Structure'),
      spacer(60),
      codeBlock([
        'shadow-send/',
        '│',
        '├── app.py              # Main Streamlit application',
        '├── requirements.txt    # Python dependencies',
        '└── README.md           # Project documentation (this file)'
      ]),

      spacer(160),

      // ── INSTALLATION ─────────────────────────────────
      heading1('⚙️ Installation & Run Locally'),
      spacer(60),

      heading3('Step 1 — Clone the repository'),
      codeBlock([
        'git clone https://github.com/your-username/shadow-send.git',
        'cd shadow-send'
      ]),

      spacer(80),
      heading3('Step 2 — Install dependencies'),
      codeBlock(['pip install -r requirements.txt']),

      spacer(80),
      heading3('Step 3 — Run the application'),
      codeBlock(['streamlit run app.py']),

      spacer(80),
      heading3('requirements.txt'),
      codeBlock([
        'streamlit',
        'cryptography',
        'numpy',
        'Pillow'
      ]),

      spacer(160),

      // ── LIVE APP ─────────────────────────────────────
      heading1('🌐 Live Application'),
      spacer(60),
      new Paragraph({
        children: [
          new TextRun({ text: '👉 ', font: 'Arial', size: 22, color: MID }),
          new ExternalHyperlink({
            link: 'https://shadow-send.streamlit.app/',
            children: [new TextRun({ text: 'https://shadow-send.streamlit.app/', font: 'Arial', size: 22, color: TEAL, underline: {} })]
          })
        ],
        spacing: { before: 60, after: 60 }
      }),

      spacer(160),

      // ── USE CASES ────────────────────────────────────
      heading1('🎯 Use Cases'),
      spacer(60),
      bullet('**Secure communication** — Send private messages hidden inside public images'),
      bullet('**Confidential information sharing** — Embed sensitive data in innocuous cover images'),
      bullet('**Digital watermarking** — Invisibly mark images with ownership or metadata'),
      bullet('**Academic / learning** — Practical demonstration of cryptography and steganography'),
      bullet('**CTF / Security challenges** — Reference implementation for hide-and-seek puzzles'),

      spacer(160),

      // ── FUTURE ENHANCEMENTS ──────────────────────────
      heading1('🚀 Future Enhancements'),
      spacer(60),
      twoColTable([
        ['User Authentication', 'Login system with user accounts and message history'],
        ['Mobile Responsive UI', 'Optimized layouts for phones and tablets'],
        ['Chat-Based Messaging', 'Real-time secure chat using stego images as carriers'],
        ['Multi-Image Support', 'Distribute a single message across multiple images'],
        ['AI Steg Detection', 'Built-in detector to test how detectable the encoding is'],
        ['Video Steganography', 'Extend LSB technique to embed data in video frames']
      ], ['Feature', 'Description']),

      spacer(160),

      // ── AUTHOR ───────────────────────────────────────
      heading1('👩‍💻 Author'),
      spacer(60),
      new Paragraph({
        children: [
          new TextRun({ text: 'Meghana S', font: 'Arial', size: 28, bold: true, color: DARK })
        ],
        spacing: { before: 60, after: 40 }
      }),
      infoBox([
        'This project demonstrates how cryptography and steganography can be combined to build',
        'a secure communication system that is both practical and user-friendly. It serves as',
        'a real-world example of applying theoretical security concepts in an accessible web app.'
      ], GREEN_BG, '16A34A', GREEN),

      spacer(160),

      // ── SUPPORT ──────────────────────────────────────
      heading1('⭐ Support'),
      spacer(60),
      para('If you find this project useful, please consider:', { spaceBefore: 60, spaceAfter: 80 }),
      bullet('⭐ **Star** this repository on GitHub'),
      bullet('🍴 **Fork** it and build your own version'),
      bullet('📢 **Share** it with others learning about cybersecurity'),
      bullet('🐛 **Open an issue** to report bugs or suggest improvements'),

      spacer(200),
      hRule(),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: 'ShadowSend PRO · Meghana S · Built with Python & Streamlit', font: 'Arial', size: 18, color: 'A0AEC0' })],
        spacing: { before: 160, after: 60 }
      })

    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('/home/claude/ShadowSend_README.docx', buf);
  console.log('Done');
}).catch(e => { console.error(e); process.exit(1); });
