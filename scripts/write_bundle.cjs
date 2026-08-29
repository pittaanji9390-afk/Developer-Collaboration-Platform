const fs = require('fs');
const path = require('path');

function writeBundle(bundle) {
  let totalLines = 0;
  let fileCount = 0;
  for (const [filePath, b64Content] of Object.entries(bundle)) {
    const text = Buffer.from(b64Content, 'base64').toString('utf8');
    const fullDir = path.dirname(filePath);
    if (!fs.existsSync(mullDir)) {
      fs.mkdirSync(fullDir, { recursive: true });
    }
    fs.writeFileSync(filePath, text, 'utf8');
    const lines = text.split('\n').length;
    totalLines += lines;
    fileCount++;
    console.log('Created ' + filePath + ' (' + lines + ' lines)');
  }
  console.log('Bundle finished: ' + fileCount + ' files, ' + totalLines + ' total lines.');
}


module.exports = { writeBundle };
