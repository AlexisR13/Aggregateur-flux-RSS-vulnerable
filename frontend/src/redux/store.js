import { configureStore } from '@reduxjs/toolkit'
import authCookieReducer from './cookies'

export default configureStore({
  reducer: {
    authCookie: authCookieReducer
  },
})