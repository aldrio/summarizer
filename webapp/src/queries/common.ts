export interface PublicError {
  error: string;
}

export function isPublicError(error: unknown): error is PublicError {
  if (typeof error !== "object" || error === null) {
    return false;
  }
  if (!("error" in error)) {
    return false;
  }

  return typeof error.error === "string";
}

export async function getResponseData<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorMessage = response.statusText;
    try {
      const data = await response.json();
      if (isPublicError(data)) {
        errorMessage = data.error;
      }
    } catch (error) {
      // ignore
    }
    throw new Error(errorMessage);
  }

  return response.json();
}

export async function apiFetch<T>(
  endpoint: string,
  init?: RequestInit
): Promise<T> {
  let response;
  try {
    response = await fetch(`${import.meta.env.VITE_API_URL}/${endpoint}`, init);
  } catch (error) {
    console.log("error???", error);
    throw new Error("There was an issue reaching the API");
  }
  return getResponseData<T>(response);
}
