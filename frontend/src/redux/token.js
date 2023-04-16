import { createSlice } from '@reduxjs/toolkit'

export const token = createSlice({
  name: 'token',
  initialState: {
    value: localStorage.getItem('token'),
  },
  reducers: {
    getToken: () => {
      const userToken = localStorage.getItem('token');
      return userToken && userToken
    },
    
    setToken: (state, object) => {
      const userToken = object.payload;
      localStorage.setItem('token', userToken);
      state.value = userToken;
    },

    removeToken: (state) => {
      localStorage.removeItem("token");
      state.value = null;
    },
  },
})

export const { getToken, setToken, removeToken } = token.actions

export default token.reducer