// Client-side helpers are for demonstrations only; Web Crypto is used for
// randomness rather than Math.random().
function generateKey(length) {
    if (!Number.isInteger(length) || length < 0) throw new Error("Invalid key length");
    const key = new Uint8Array(length);
    crypto.getRandomValues(key);
    return key;
}

function otpEncrypt(text, key) {
    const data = new TextEncoder().encode(text);
    if (data.length !== key.length) throw new Error("Key length must match UTF-8 data length");
    return data.map((value, index) => value ^ key[index]);
}
