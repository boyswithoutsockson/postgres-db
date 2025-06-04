export function encode(str: string): string {
  return encodeURIComponent(str).replace(/%20/g, '+');
}

export function decode(str: string): string {
  return decodeURIComponent(str.replace(/\+/g, '%20'));
}
