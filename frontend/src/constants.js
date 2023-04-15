const dev_url = 'http://localhost:5000';
const prod_url = 'http://server:5000/api';

export const BACKEND_URL = process.env.NODE_ENV === 'prod' ? prod_url : dev_url;