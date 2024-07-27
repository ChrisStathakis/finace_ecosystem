import axios from 'axios';
import { jwtDecode } from "jwt-decode";
import { BASE_URL, REFRESH_TOKEN_ENDPOINT } from './endpoints';
import { ACCESS_TOKEN, REFRESH_TOKEN } from './actionTypes';
import store from "./store"
import { logout_action } from './slices/userSlice';

// Function to refresh the token
async function refreshToken() {
    try {
        const response = await axios.post(REFRESH_TOKEN_ENDPOINT, {
            refresh: localStorage.getItem(REFRESH_TOKEN)
        });

        const { access } = response.data;

        // Save the new access token
        localStorage.setItem(ACCESS_TOKEN, access);

        // Update the Axios instance with the new access token
        axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${access}`;

        return access;
    } catch (error) {
        console.error('Failed to refresh token', error);
        console.log("refresh", localStorage.getItem(REFRESH_TOKEN))
        // Handle token refresh failure (e.g., redirect to login)
        throw error;
    }
}

// Function to check if the token is close to expiry
function isTokenExpired(token) {
    if (!token) return true;
    const { exp } = jwtDecode(token);
    // Check if token will expire in the next minute
    return (exp * 1000 - Date.now()) < 60000;
}

// Create Axios instance
const axiosInstance = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Authorization': `Bearer ${localStorage.getItem(ACCESS_TOKEN)}`
    }
});

// Add a request interceptor to refresh the token if it's close to expiry
axiosInstance.interceptors.request.use(
    async config => {
        let token = localStorage.getItem(ACCESS_TOKEN);
        console.log("access token", token)
        if (isTokenExpired(token)) {
            token = await refreshToken();
        }

        config.headers['Authorization'] = `Bearer ${token}`;
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// Add a response interceptor to handle 401 errors
axiosInstance.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const newAccessToken = await refreshToken();
                originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
                return axiosInstance(originalRequest);
            } catch (refreshError) {
                store.dispatch(logout_action());
                window.location.href = "/login";
                
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default axiosInstance;
