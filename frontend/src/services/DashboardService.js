import api from "./api";

export const getDashboard = async () => {
    const response = await api.get("/employees/dashboard");
    return response.data;
};