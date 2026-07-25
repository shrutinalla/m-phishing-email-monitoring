import api from "./api";

export const getEmployees = async () => {
    const response = await api.get("/employees");
    return response.data;
};

export const addEmployee = async (employee) => {
    const response = await api.post("/employees", employee);
    return response.data;
};

export const deleteEmployee = async (id) => {
    const response = await api.delete(`/employees/${id}`);
    return response.data;
};

export const searchEmployees = async (keyword) => {
    const response = await api.get(`/employees/search?keyword=${keyword}`);
    return response.data;
};