import { createSlice } from '@reduxjs/toolkit'
import Cookies from 'js-cookie';

export const authCookie = createSlice({
  name: 'authCookie',
  initialState: {
    value: Cookies.get('username'),
  },
  reducers: {
    setAuthCookie: (state, object) => {
      const cookieValue = object.payload
      Cookies.set('username', cookieValue);
      state.value = cookieValue;
    },
    removeAuthCookie: (state) => {
      Cookies.remove('username');
      state.value = undefined;
    }
  },
})

export const { setAuthCookie, removeAuthCookie } = authCookie.actions

export default authCookie.reducer