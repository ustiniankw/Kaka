// Simple icon generator for Kaka extension.
// Writes tiny placeholder PNGs from base64 data.
const fs = require('fs');
const path = require('path');

// 1x1 transparent PNG (data URL body), OK 作为占位图标
const B64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII=';

['icon16.png','icon48.png','icon128.png'].forEach(name => {
  const p = path.join(__dirname, name);
  fs.writeFileSync(p, Buffer.from(B64, 'base64'));
  console.log('wrote', p);
});
