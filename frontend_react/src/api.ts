import axios from 'axios';

const API_URL = "http://localhost:8000/orders";

export const fetchOrders = async (page: number, pageSize: number) => {
    const response = await axios.get(`${API_URL}/?page=${page}&page_size=${pageSize}`);
    return response.data;
};

// export const createOrder = async (orderData: any) => {
//     const response = await axios.post(API_URL, orderData);
//     return response.data;
// };
//
// export const updateOrder = async (id: string, updatedData: any) => {
//     const response = await axios.put(`${API_URL}/${id}/`, updatedData);
//     return response.data;
// };
//
// export const deleteOrder = async (id: string) => {
//     await axios.delete(`${API_URL}/${id}/`);
// };
