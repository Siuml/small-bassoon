// utils/crypto.js
const jsSHA = require('./sha256.js');

const Crypto = {
  hmacsha256: function(content, key) {
    const shaObj = new jsSHA("SHA-256", "TEXT");
    shaObj.setHMACKey(key, "TEXT");
    shaObj.update(content);
    return shaObj.getHMAC("HEX");
  }
};

module.exports = Crypto; // 唯一导出