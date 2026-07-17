// Simple icon generator for Kaka desktop.
// Writes placeholder PNG + ICO + ICNS from base64 data.
const fs = require('fs');
const path = require('path');

const outDir = path.join(__dirname, 'build');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

// 128x128 orange square PNG
const PNG128_B64 = 'iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAABT0lEQVR4nO3SMQEAIAzAMMD/i94hg6OJgh7dc9csss7vAP4yQJwB4gwQZ4A4A8QZIM4AcQaIM0CcAeIMEGeAOAPEGSDOAHEGiDNAnAHiDBBngDgDxBkgzgBxBogzQJwB4gwQZ4A4A8QZIM4AcQaIM0CcAeIMEGeAOAPEGSDOAHEGiDNAnAHiDBBngDgDxBkgzgBxBogzQJwB4gwQZ4A4A8QZIM4AcQaIM0CcAeIMEGeAOAPEGSDOAHEGiDNAnAHiDBBngDgDxBkgzgBxBogzQJwB4gwQZ4A4A8QZIM4AcQaIM0CcAeIMEGeAOAPEGSDOAHEGiDNAnAHiDBBngDgDxBkgzgBxBogzQJwB4gwQZ4A4A8QZIM4AcQaIM0CcAeIMEGeAOAPEGSDOAHEGiDNAnAHiDBBngDgDxBkgzgBxBogzQJwB4gwQZIO4BshYDkyXkAUkAAAAASUVORK5CYII=';
// 32x32 orange square PNG
const PNG32_B64 = 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAMElEQVR4nO3OMQEAIAzAsIL/F71Dxp7UQHPmNS12N+cAAAAAAAAAAAAAAAAAAABVH5LgAtOwSd8aAAAAAElFTkSuQmCC';

function writeBin(name, buf) {
  const p = path.join(outDir, name);
  fs.writeFileSync(p, buf);
  console.log('wrote', p);
}

function makeIcoFromPng(pngBuf, size) {
  // ICO header (6) + dir entry (16) + png data
  const header = Buffer.alloc(6);
  header.writeUInt16LE(0, 0);      // reserved
  header.writeUInt16LE(1, 2);      // type = icon
  header.writeUInt16LE(1, 4);      // count

  const dir = Buffer.alloc(16);
  dir.writeUInt8(size === 256 ? 0 : size, 0); // width
  dir.writeUInt8(size === 256 ? 0 : size, 1); // height
  dir.writeUInt8(0, 2);  // colors
  dir.writeUInt8(0, 3);  // reserved
  dir.writeUInt16LE(1, 4);   // planes
  dir.writeUInt16LE(32, 6);  // bitcount
  dir.writeUInt32LE(pngBuf.length, 8);
  dir.writeUInt32LE(6 + 16, 12);   // offset

  return Buffer.concat([header, dir, pngBuf]);
}

function makeIcnsFromPng(pngBuf) {
  // Minimal ICNS: header + a single ic07 chunk (128x128 PNG)
  const type = Buffer.from('ic07');
  const chunkLen = Buffer.alloc(4);
  chunkLen.writeUInt32BE(8 + pngBuf.length, 0);
  const chunk = Buffer.concat([type, chunkLen, pngBuf]);

  const hdr = Buffer.from('icns');
  const totalLen = Buffer.alloc(4);
  totalLen.writeUInt32BE(8 + chunk.length, 0);

  return Buffer.concat([hdr, totalLen, chunk]);
}

const png128 = Buffer.from(PNG128_B64, 'base64');
const png32 = Buffer.from(PNG32_B64, 'base64');

writeBin('icon.png', png128);
writeBin('tray.png', png32);
writeBin('icon.ico', makeIcoFromPng(png128, 128));
writeBin('icon.icns', makeIcnsFromPng(png128));
