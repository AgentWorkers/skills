const nodemailer = require('nodemailer');
const imaps = require('imap-simple');

const CONFIG = {
    user: 'info@pestward.com',
    pass: 'sgSPL50i5mke', // Provided by user
    hostImap: 'imap.zoho.com',
    portImap: 993,
    hostSmtp: 'smtp.zoho.com',
    portSmtp: 465, // SSL
    secureSmtp: true
};

async function sendEmail(args) {
    const { to, subject, body, cc, bcc } = args;

    const transporter = nodemailer.createTransport({
        host: CONFIG.hostSmtp,
        port: CONFIG.portSmtp,
        secure: CONFIG.secureSmtp,
        auth: {
            user: CONFIG.user,
            pass: CONFIG.pass
        }
    });

    const info = await transporter.sendMail({
        from: `"Pestward Info" <${CONFIG.user}>`,
        to,
        subject,
        html: body,
        cc,
        bcc
    });

    return `Email sent: ${info.messageId}`;
}

async function searchEmails(args) {
    const { query, limit = 10, markRead = false } = args;

    const connection = await imaps.connect({
        imap: {
            user: CONFIG.user,
            password: CONFIG.pass,
            host: CONFIG.hostImap,
            port: CONFIG.portImap,
            tls: true,
            authTimeout: 3000
        }
    });

    await connection.openBox('INBOX');

    // Simple search (UNSEEN, etc.) - complex queries might need parsing
    // For now, support simple "UNSEEN" or generic keyword search
    let searchCriteria = ['UNSEEN']; 
    if (query && query !== 'UNSEEN') {
        // If specific criteria provided, use it (simplified for now)
        // Ideally parse "from:foo" to ['FROM', 'foo']
        // Fallback to text search on BODY/SUBJECT
        searchCriteria = [['OR', ['SUBJECT', query], ['BODY', query]]];
    }

    const fetchOptions = {
        bodies: ['HEADER', 'TEXT', ''],
        markSeen: markRead
    };

    const messages = await connection.search(searchCriteria, fetchOptions);
    
    // Sort recent first and limit
    const results = messages.reverse().slice(0, limit).map(item => {
        const subject = item.parts.find(p => p.which === 'HEADER').body.subject[0];
        const from = item.parts.find(p => p.which === 'HEADER').body.from[0];
        const date = item.parts.find(p => p.which === 'HEADER').body.date[0];
        const body = item.parts.find(p => p.which === 'TEXT')?.body || '(No text body)';
        return `From: ${from}\nDate: ${date}\nSubject: ${subject}\nBody: ${body.substring(0, 200)}...`;
    });

    connection.end();
    return results.length > 0 ? results.join('\n---\n') : 'No matching emails found.';
}

// Simple export for potential direct use or testing
module.exports = { sendEmail, searchEmails };

// Basic CLI runner for the skill (OpenClaw style)
if (require.main === module) {
    const args = process.argv.slice(2);
    const command = args[0];
    const jsonArgs = args[1] ? JSON.parse(args[1]) : {};

    if (command === 'send') {
        sendEmail(jsonArgs).then(console.log).catch(console.error);
    } else if (command === 'search') {
        searchEmails(jsonArgs).then(console.log).catch(console.error);
    } else {
        console.log('Usage: node index.js <send|search> <json-args>');
    }
}
