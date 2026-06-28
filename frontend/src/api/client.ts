/**
 * API client — base fetch wrapper with error handling.
 */

const API_BASE = 'http://localhost:8000/api';

interface ApiError {
  detail: string;
}

async function apiFetch<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const error: ApiError = await response.json().catch(() => ({
      detail: `Erreur HTTP ${response.status}`,
    }));
    throw new Error(error.detail);
  }

  return response.json();
}

export { apiFetch, API_BASE };
