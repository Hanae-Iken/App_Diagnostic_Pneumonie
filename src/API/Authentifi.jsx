export const register = async (userData) => {
  try {
    const response = await API.post('/register', userData);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const login = async (credentials) => {
  try {
    const response = await API.post('/login', credentials);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const resetPassword = async (email) => {
  try {
    const response = await API.post('/reset-password', { email });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};