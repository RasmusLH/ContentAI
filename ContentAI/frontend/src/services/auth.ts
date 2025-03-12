import { User } from '../types';

export interface AuthResponse {
  user: User;
  token: string;
}

const AUTH_BASE_URL = "http://localhost:8000/api/auth";

export const loginWithGoogle = async (googleToken: string): Promise<AuthResponse> => {
  const response = await fetch(`${AUTH_BASE_URL}/google`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ token: googleToken }),
  });

  if (!response.ok) {
    throw new Error('Authentication failed');
  }

  return response.json();
};

export const logout = async (): Promise<void> => {
  localStorage.removeItem('authToken');
  localStorage.removeItem('user');
};
