const dev_url = 'http://localhost:5000';
const prod_url = 'http://localhost:8080/api';

export const BACKEND_URL = process.env.NODE_ENV === 'production' ? prod_url : dev_url;