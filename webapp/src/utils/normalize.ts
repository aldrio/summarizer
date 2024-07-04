/**
 * Normalize a URL by adding the scheme if it's missing
 */
export function normalizeUrl(url: string) {
  const withoutScheme = url.replace(/https?:\/\//, "");
  return `https://${withoutScheme}`;
}

/**
 * Check if a string is a valid URL
 */
export function isValidUrl(url: string) {
  try {
    new URL(normalizeUrl(url));
    return true;
  } catch (e) {
    return false;
  }
}
